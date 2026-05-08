"""
Optional batch step: generate model_responses.csv from prompts via an API.

Requires the `openai` package and environment variables (see README).
No API keys are stored in the repository.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path


def dry_run_rows(test_cases_path: Path) -> list[tuple[str, str]]:
    """Build placeholder responses for local testing without network."""
    rows: list[tuple[str, str]] = []
    with test_cases_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row["case_id"]
            placeholder = (
                f"[DRY RUN] No API call made. Replace this text with a real model response for {cid}."
            )
            rows.append((cid, placeholder))
    return rows


def write_responses_csv(out_path: Path, rows: list[tuple[str, str]]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "model_response"])
        w.writerows(rows)


def collect_via_openai(test_cases_path: Path, model: str, temperature: float) -> list[tuple[str, str]]:
    """Call Chat Completions for each prompt. Uses OPENAI_API_KEY from the environment."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit(
            "Install the optional dependency: pip install '.[model]' "
            "(adds the openai package)."
        ) from exc

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL") or None,
    )
    rows: list[tuple[str, str]] = []
    with test_cases_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row["prompt"]
            completion = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You answer patient health questions cautiously. "
                            "You are not a substitute for a clinician."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            text = completion.choices[0].message.content or ""
            rows.append((row["case_id"], text.strip()))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create model_responses.csv from test_cases.csv using an API or dry-run placeholders."
    )
    parser.add_argument(
        "--test-cases",
        type=Path,
        required=True,
        help="Path to test_cases.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to write model_responses.csv",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write placeholder responses without calling any API.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.environ.get("EVAL_MODEL_NAME", "gpt-4o-mini"),
        help="Model name when using the API (default from EVAL_MODEL_NAME or gpt-4o-mini).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=float(os.environ.get("EVAL_TEMPERATURE", "0.2")),
        help="Sampling temperature for API calls.",
    )
    args = parser.parse_args()

    if args.dry_run:
        rows = dry_run_rows(args.test_cases)
        write_responses_csv(args.output, rows)
        print(f"Wrote {len(rows)} placeholder rows to {args.output}")
        return

    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "OPENAI_API_KEY is not set. Use --dry-run for placeholders, or export the key.",
            file=sys.stderr,
        )
        sys.exit(1)

    rows = collect_via_openai(args.test_cases, args.model, args.temperature)
    write_responses_csv(args.output, rows)
    print(f"Wrote {len(rows)} API responses to {args.output}")


if __name__ == "__main__":
    main()
