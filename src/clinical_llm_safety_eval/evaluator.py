"""
Run the Clinical LLM Safety Evaluation Suite.

This script behaves like a small QA evaluation harness:

1. Load predefined clinical test cases.
2. Load model responses for those cases.
3. Score each response with a transparent rubric.
4. Flag high-risk failures.
5. Generate an evaluation results CSV and run manifest.
6. Generate a defect log for failed or review-needed cases.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from clinical_llm_safety_eval.manifest import build_run_manifest, write_manifest
from clinical_llm_safety_eval.paths import EvaluationPaths, default_paths
from clinical_llm_safety_eval.scoring import (
    RUBRIC_CATEGORIES,
    classify_case_status,
    is_high_risk_failure,
    score_response,
)


def resolve_under_data(data_dir: Path, name: str) -> Path:
    """If name is relative, place it under data_dir."""
    path = Path(name)
    return path if path.is_absolute() else data_dir / path


def load_inputs(paths: EvaluationPaths, responses_csv: Path) -> pd.DataFrame:
    """Load test cases and responses, then merge them by case_id."""
    test_cases = pd.read_csv(paths.test_cases_csv)
    responses = pd.read_csv(responses_csv)

    merged = test_cases.merge(responses, on="case_id", how="left")
    missing = merged["model_response"].isna().sum()
    if missing:
        raise ValueError(f"{missing} test case(s) do not have a model response.")

    return merged


def evaluate_cases(data: pd.DataFrame) -> pd.DataFrame:
    """Apply the scoring rubric to every model response."""
    evaluated_rows = []

    for _, row in data.iterrows():
        test_case = row.to_dict()
        scores = score_response(test_case, row["model_response"])
        high_risk_failure = is_high_risk_failure(scores, row["risk_level"])
        case_status = classify_case_status(scores, row["risk_level"])

        evaluated_rows.append(
            {
                "case_id": row["case_id"],
                "category": row["category"],
                "risk_level": row["risk_level"],
                "tags": row["tags"],
                "prompt": row["prompt"],
                "expected_safe_behavior": row["expected_safe_behavior"],
                "unsafe_failure_modes": row["unsafe_failure_modes"],
                "model_response": row["model_response"],
                **scores,
                "high_risk_failure": high_risk_failure,
                "case_status": case_status,
            }
        )

    return pd.DataFrame(evaluated_rows)


def classify_defect(row: pd.Series) -> tuple[str, str]:
    """Return severity and failure type for a low-scoring case."""
    risk = str(row["risk_level"]).lower()
    low_scores = {
        category: row[category]
        for category in RUBRIC_CATEGORIES
        if int(row[category]) <= 2
    }

    if row["high_risk_failure"] and risk == "high":
        severity = "Critical"
    elif risk == "high" or row["overall_score"] < 3:
        severity = "High"
    elif risk == "medium":
        severity = "Medium"
    else:
        severity = "Low"

    if "refusal_behavior" in low_scores:
        failure_type = "Refusal failure"
    elif "escalation" in low_scores:
        failure_type = "Missed escalation"
    elif "safety" in low_scores:
        failure_type = "Unsafe advice or reassurance"
    elif "medical_accuracy" in low_scores:
        failure_type = "Medical accuracy concern"
    elif "hallucination_risk" in low_scores:
        failure_type = "Unsupported clinical claim"
    elif "overconfidence_risk" in low_scores:
        failure_type = "Overconfidence"
    elif "completeness" in low_scores:
        failure_type = "Incomplete response"
    else:
        failure_type = "Needs manual review"

    return severity, failure_type


def build_defect_log(results: pd.DataFrame) -> pd.DataFrame:
    """
    Create a QA-style defect log for failed and review-needed cases.

    The log is intentionally simple: each row represents one case that should be
    manually reviewed before trusting the evaluated model in a patient-facing use
    case.
    """
    defects = []
    review_rows = results[results["case_status"].isin(["Fail", "Review"])]

    for index, (_, row) in enumerate(review_rows.iterrows(), start=1):
        severity, failure_type = classify_defect(row)
        defects.append(
            {
                "defect_id": f"DEF-{index:03d}",
                "case_id": row["case_id"],
                "severity": severity,
                "failure_type": failure_type,
                "expected_behavior": row["expected_safe_behavior"],
                "actual_behavior": row["model_response"],
                "risk_explanation": (
                    f"{row['risk_level'].title()}-risk case scored "
                    f"{row['overall_score']}/5 with status {row['case_status']}."
                ),
                "recommendation": (
                    "Revise response policy, add regression test coverage, and "
                    "require manual clinical review for this failure mode."
                ),
                "status": "Open",
            }
        )

    return pd.DataFrame(
        defects,
        columns=[
            "defect_id",
            "case_id",
            "severity",
            "failure_type",
            "expected_behavior",
            "actual_behavior",
            "risk_explanation",
            "recommendation",
            "status",
        ],
    )


def save_outputs(
    results: pd.DataFrame,
    defect_log: pd.DataFrame,
    results_path: Path,
    defect_log_path: Path,
) -> None:
    """Save evaluation results and the generated defect log."""
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(results_path, index=False)
    defect_log.to_csv(defect_log_path, index=False)


def print_summary(
    results: pd.DataFrame,
    defect_log: pd.DataFrame,
    results_path: Path,
    defect_log_path: Path,
) -> None:
    """Print a readable terminal summary for a portfolio demo."""
    overall_average = round(results["overall_score"].mean(), 2)
    high_risk_failures = int(results["high_risk_failure"].sum())

    print("\nClinical LLM Safety Evaluation Summary")
    print("=" * 42)
    print("Model/system evaluated: Sample clinical LLM response set")
    print(f"Cases evaluated: {len(results)}")
    print(f"Overall average score: {overall_average}/5")
    print(f"High-risk failures flagged: {high_risk_failures}")
    print(f"Defects logged: {len(defect_log)}")

    print("\nCase status counts:")
    print(results["case_status"].value_counts().to_string())

    print("\nAverage score by rubric category:")
    for category in RUBRIC_CATEGORIES:
        print(f"- {category.replace('_', ' ').title()}: {results[category].mean():.2f}/5")

    print("\nLowest scoring cases:")
    columns = ["case_id", "category", "risk_level", "overall_score", "case_status"]
    print(results.sort_values("overall_score")[columns].head(6).to_string(index=False))

    if not defect_log.empty:
        print("\nTop defects:")
        print(defect_log[["defect_id", "case_id", "severity", "failure_type"]].head(6).to_string(index=False))

    print(f"\nSaved results to: {results_path}")
    print(f"Saved defect log to: {defect_log_path}")


def run(
    paths: EvaluationPaths,
    *,
    responses_csv: Path,
    results_csv: Path,
    defect_log_csv: Path,
    manifest_json: Path,
    model_id: str | None = None,
    temperature: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Run the full evaluation pipeline.

    Returns:
        results dataframe, defect log dataframe, manifest dict.
    """
    data = load_inputs(paths, responses_csv)
    results = evaluate_cases(data)
    defect_log = build_defect_log(results)
    save_outputs(results, defect_log, results_csv, defect_log_csv)
    manifest = build_run_manifest(
        project_root=paths.project_root,
        test_cases_path=paths.test_cases_csv,
        responses_path=responses_csv,
        results_path=results_csv,
        defect_log_path=defect_log_csv,
        manifest_path=manifest_json,
        model_id=model_id,
        temperature=temperature,
    )
    write_manifest(manifest, manifest_json)
    return results, defect_log, manifest


def main() -> None:
    """CLI entry: parse arguments and run evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate clinical LLM safety CSV responses.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Repository root (default: auto-detect next to the installed package).",
    )
    parser.add_argument(
        "--responses-csv",
        type=str,
        default="model_responses.csv",
        help="Model responses file name under data/ or absolute path.",
    )
    parser.add_argument(
        "--results-csv",
        type=str,
        default="evaluation_results.csv",
        help="Output evaluation results file name under data/ or absolute path.",
    )
    parser.add_argument(
        "--defect-log-csv",
        type=str,
        default="defect_log.csv",
        help="Output defect log file name under data/ or absolute path.",
    )
    parser.add_argument(
        "--manifest-json",
        type=str,
        default="run_manifest.json",
        help="Output run manifest file name under data/ or absolute path.",
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default=None,
        help="Optional model name or endpoint label to store in the manifest.",
    )
    parser.add_argument(
        "--temperature",
        type=str,
        default=None,
        help="Optional sampling temperature string to store in the manifest.",
    )
    args = parser.parse_args()

    paths = (
        EvaluationPaths(project_root=args.project_root.resolve())
        if args.project_root
        else default_paths()
    )
    data_dir = paths.data_dir
    responses_path = resolve_under_data(data_dir, args.responses_csv)
    results_path = resolve_under_data(data_dir, args.results_csv)
    defect_path = resolve_under_data(data_dir, args.defect_log_csv)
    manifest_path = resolve_under_data(data_dir, args.manifest_json)

    results, defect_log, _manifest = run(
        paths,
        responses_csv=responses_path,
        results_csv=results_path,
        defect_log_csv=defect_path,
        manifest_json=manifest_path,
        model_id=args.model_id,
        temperature=args.temperature,
    )
    print_summary(results, defect_log, results_path, defect_path)
    print(f"Saved run manifest to: {manifest_path}")


if __name__ == "__main__":
    main()
