"""
Compare two evaluation result CSVs (e.g. two models or two prompt configs).

Joins on case_id and summarizes regressions and improvements.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def _df_to_markdown_table(df: pd.DataFrame) -> str:
    """Small Markdown table without optional tabulate dependency."""
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in headers) + " |")
    return "\n".join(lines)


def compare_dataframes(a: pd.DataFrame, b: pd.DataFrame, label_a: str, label_b: str) -> str:
    """Build a Markdown comparison of two evaluation_results tables."""
    merged = a.merge(
        b,
        on="case_id",
        suffixes=("_a", "_b"),
        how="outer",
        validate="one_to_one",
    )
    lines: list[str] = [
        "# Evaluation run comparison",
        "",
        f"- Run A: **{label_a}**",
        f"- Run B: **{label_b}**",
        "",
        "## Summary",
        "",
        "| Metric | Run A | Run B | Delta (B - A) |",
        "| --- | --- | --- | --- |",
    ]

    def count_fail(df: pd.DataFrame, col: str) -> int:
        return int((df[col] == "Fail").sum())

    def count_high_risk(df: pd.DataFrame, col: str) -> int:
        series = df[col].map(lambda x: str(x).lower() in ("true", "1", "yes"))
        return int(series.sum())

    fa = count_fail(a, "case_status")
    fb = count_fail(b, "case_status")
    lines.append(f"| Fail count | {fa} | {fb} | {fb - fa:+d} |")

    ha = count_high_risk(a, "high_risk_failure")
    hb = count_high_risk(b, "high_risk_failure")
    lines.append(f"| high_risk_failure true | {ha} | {hb} | {hb - ha:+d} |")

    ma = round(a["overall_score"].mean(), 3)
    mb = round(b["overall_score"].mean(), 3)
    lines.append(f"| Mean overall_score | {ma} | {mb} | {round(mb - ma, 3):+f} |")
    lines.extend(["", "## Regressions (Run B worse than Run A)", ""])

    critical_dims = ["safety", "escalation", "refusal_behavior", "medical_accuracy"]
    regression_ids: list[str] = []
    for _, row in merged.iterrows():
        oa = row.get("overall_score_a")
        ob = row.get("overall_score_b")
        if pd.isna(oa) or pd.isna(ob):
            continue
        worse_overall = float(ob) < float(oa) - 0.01
        worse_critical = False
        for dim in critical_dims:
            va = row.get(f"{dim}_a")
            vb = row.get(f"{dim}_b")
            if pd.notna(va) and pd.notna(vb) and int(vb) < int(va):
                worse_critical = True
                break
        if worse_overall or worse_critical:
            regression_ids.append(str(row["case_id"]))

    uniq = regression_ids[:30]
    if not regression_ids:
        lines.append("No regressions detected by overall or critical dimension drop.")
    else:
        lines.extend([f"- `{cid}`" for cid in uniq])
        if len(regression_ids) > 30:
            lines.append(f"- … and {len(regression_ids) - 30} more")

    lines.extend(["", "## Side-by-side (first 12 cases)", ""])
    cols = ["case_id", "overall_score_a", "overall_score_b", "case_status_a", "case_status_b"]
    sample = merged[cols].head(12)
    lines.append(_df_to_markdown_table(sample))
    return "\n".join(lines)


def write_comparison_report(path_a: Path, path_b: Path, out: Path, label_a: str, label_b: str) -> None:
    """Load two evaluation CSVs and write Markdown."""
    df_a = pd.read_csv(path_a)
    df_b = pd.read_csv(path_b)
    md = compare_dataframes(df_a, df_b, label_a, label_b)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two evaluation_results.csv files.")
    parser.add_argument("--a", type=Path, required=True, help="First evaluation_results.csv")
    parser.add_argument("--b", type=Path, required=True, help="Second evaluation_results.csv")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output Markdown path (default: reports/run_comparison.md next to cwd).",
    )
    parser.add_argument("--label-a", type=str, default="Run A")
    parser.add_argument("--label-b", type=str, default="Run B")
    args = parser.parse_args()

    out = args.out or Path("reports/run_comparison.md")
    if not out.is_absolute():
        out = Path.cwd() / out
    write_comparison_report(args.a, args.b, out, args.label_a, args.label_b)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
