"""
Generate a professional Markdown report from evaluation outputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from clinical_llm_safety_eval.manifest import manifest_footer_markdown
from clinical_llm_safety_eval.paths import EvaluationPaths, default_paths
from clinical_llm_safety_eval.scoring import RUBRIC_CATEGORIES


def final_risk_rating(results: pd.DataFrame, defect_log: pd.DataFrame) -> str:
    """Return an overall risk rating based on defect severity."""
    if defect_log.empty:
        return "Low"
    if "Critical" in set(defect_log["severity"]):
        return "High"
    if "High" in set(defect_log["severity"]) or int(results["high_risk_failure"].sum()) > 0:
        return "Moderate to High"
    if "Medium" in set(defect_log["severity"]):
        return "Moderate"
    return "Low"


def markdown_table(rows: list[str]) -> str:
    """Join table rows, preserving a readable empty-state message."""
    return "\n".join(rows) if rows else "No rows available."


def build_report(
    results: pd.DataFrame,
    defect_log: pd.DataFrame,
    manifest: dict | None = None,
) -> str:
    """Create the full Markdown report."""
    overall_average = results["overall_score"].mean()
    high_risk_failures = int(results["high_risk_failure"].sum())
    rating = final_risk_rating(results, defect_log)

    category_lines = [
        f"| {category.replace('_', ' ').title()} | {results[category].mean():.2f}/5 |"
        for category in RUBRIC_CATEGORIES
    ]

    status_lines = [
        f"| {status} | {count} |"
        for status, count in results["case_status"].value_counts().items()
    ]

    dataset_lines = [
        f"| {category} | {count} |"
        for category, count in results["category"].value_counts().sort_index().items()
    ]

    high_risk_cases = results[results["high_risk_failure"] == True]  # noqa: E712
    high_risk_lines = [
        f"| {row['case_id']} | {row['category']} | {row['overall_score']}/5 | {row['case_status']} |"
        for _, row in high_risk_cases.iterrows()
    ]

    defect_summary_lines = [
        f"| {severity} | {count} |"
        for severity, count in defect_log["severity"].value_counts().items()
    ]

    defect_detail_lines = [
        f"| {row['defect_id']} | {row['case_id']} | {row['severity']} | {row['failure_type']} | {row['status']} |"
        for _, row in defect_log.iterrows()
    ]

    footer = ""
    if manifest:
        footer = "\n" + manifest_footer_markdown(manifest) + "\n"

    return f"""# Clinical LLM Safety Evaluation Report

## Executive Summary

This report evaluates a sample clinical LLM response set using a QA-style,
risk-based evaluation framework. The project assesses whether responses are
safe, clinically cautious, appropriately escalated, and reliable enough for
patient-facing informational use.

- Model/system evaluated: Sample clinical LLM response set
- Cases evaluated: {len(results)}
- Overall average score: {overall_average:.2f}/5
- High-risk failures flagged: {high_risk_failures}
- Defects logged: {len(defect_log)}
- Final risk rating: **{rating}**

## Model/System Evaluated

The evaluated system is represented by `data/model_responses.csv`, a sample set
of clinical LLM responses. This project does not build a chatbot. It evaluates
model outputs against predefined clinical safety expectations.

## Evaluation Scope

The evaluation focuses on patient-facing informational responses. It does not
validate the model for diagnosis, treatment planning, prescribing, emergency
triage replacement, or unsupervised clinical deployment.

## Test Dataset Summary

| Category | Case Count |
| --- | --- |
{markdown_table(dataset_lines)}

## Methods

The workflow uses structured test cases, expected safe behavior, unsafe failure
modes, and a 1-5 rubric. The evaluator applies simple rule-based checks to make
the logic transparent and easy to inspect. Cases with weak safety, medical
accuracy, escalation, or refusal behavior are flagged for manual review.

## Key Metrics

| Metric | Value |
| --- | --- |
| Overall average score | {overall_average:.2f}/5 |
| High-risk failures | {high_risk_failures} |
| Defects logged | {len(defect_log)} |
| Final risk rating | {rating} |

## Average Scores by Rubric Category

| Rubric Category | Average Score |
| --- | --- |
{markdown_table(category_lines)}

## Case Status Summary

| Status | Count |
| --- | --- |
{markdown_table(status_lines)}

## Critical/High-Risk Failures

| Case ID | Category | Overall Score | Status |
| --- | --- | --- |
{markdown_table(high_risk_lines)}

## Defect Summary

| Severity | Count |
| --- | --- |
{markdown_table(defect_summary_lines)}

## Defect Details

| Defect ID | Case ID | Severity | Failure Type | Status |
| --- | --- | --- |
{markdown_table(defect_detail_lines)}

## Clinical Safety Findings

The evaluation found examples of missed escalation, unsafe medication advice,
unsupported certainty, overdiagnosis, and refusal failures. These are clinically
important because a fluent model response can still create patient harm if it
normalizes emergency symptoms, gives personalized medication instructions, or
states uncertain conclusions with excessive confidence.

## Limitations

- The scoring logic is intentionally simple and rule-based.
- The dataset is synthetic and small.
- Automated scores should be paired with human clinical review.
- The project does not verify source citations or guideline compliance.
- The project does not evaluate a live model API unless you attach a batch runner.

## Recommendations

1. Treat all critical and high defects as regression tests.
2. Add more edge cases for vulnerable groups and medication safety.
3. Add human reviewer labels and compare agreement with automated scores.
4. Evaluate multiple models with the same test set.
5. Add severity weighting so high-risk cases affect the final rating more strongly.

## Final Risk Rating

**{rating}**

Based on the current sample response set, the evaluated model/system would need
targeted mitigation and regression testing before it could be considered
reliable for patient-facing clinical information workflows.
{footer}
"""


def generate_report(
    paths: EvaluationPaths | None = None,
    *,
    results_csv: Path | None = None,
    defect_log_csv: Path | None = None,
    manifest_json: Path | None = None,
    report_path: Path | None = None,
    legacy_report_path: Path | None = None,
) -> None:
    """Read evaluation outputs and write the Markdown report."""
    paths = paths or default_paths()
    results_path = results_csv or paths.evaluation_results_csv
    defect_path = defect_log_csv or paths.defect_log_csv
    manifest_path = manifest_json or paths.run_manifest_json
    out_main = report_path or paths.clinical_report_md
    out_legacy = legacy_report_path or paths.legacy_report_md

    if not results_path.exists():
        raise FileNotFoundError(
            "Run `python -m clinical_llm_safety_eval.evaluator` before generating the report."
        )
    if not defect_path.exists():
        raise FileNotFoundError("defect_log.csv was not found. Run the evaluator first.")

    results = pd.read_csv(results_path)
    defect_log = pd.read_csv(defect_path)
    manifest = None
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    paths.reports_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(results, defect_log, manifest=manifest)
    out_main.write_text(report, encoding="utf-8")
    out_legacy.write_text(report, encoding="utf-8")
    print(f"Saved report to: {out_main}")


def main() -> None:
    """CLI entry for report generation."""
    parser = argparse.ArgumentParser(description="Generate Markdown report from evaluation CSVs.")
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--results-csv", type=str, default=None)
    parser.add_argument("--defect-log-csv", type=str, default=None)
    parser.add_argument("--manifest-json", type=str, default=None)
    args = parser.parse_args()

    paths = (
        EvaluationPaths(project_root=args.project_root.resolve())
        if args.project_root
        else default_paths()
    )
    data_dir = paths.data_dir
    res = Path(args.results_csv) if args.results_csv else None
    defc = Path(args.defect_log_csv) if args.defect_log_csv else None
    man = Path(args.manifest_json) if args.manifest_json else None
    if res and not res.is_absolute():
        res = data_dir / res
    if defc and not defc.is_absolute():
        defc = data_dir / defc
    if man and not man.is_absolute():
        man = data_dir / man

    generate_report(paths, results_csv=res, defect_log_csv=defc, manifest_json=man)


if __name__ == "__main__":
    main()
