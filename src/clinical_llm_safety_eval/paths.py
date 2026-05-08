"""Filesystem locations for the evaluation harness."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class EvaluationPaths:
    """Paths rooted at the repository (project) root."""

    project_root: Path

    @property
    def data_dir(self) -> Path:
        """Directory for CSV inputs and outputs."""
        return self.project_root / "data"

    @property
    def reports_dir(self) -> Path:
        """Directory for Markdown reports."""
        return self.project_root / "reports"

    @property
    def test_cases_csv(self) -> Path:
        return self.data_dir / "test_cases.csv"

    @property
    def model_responses_csv(self) -> Path:
        return self.data_dir / "model_responses.csv"

    @property
    def evaluation_results_csv(self) -> Path:
        return self.data_dir / "evaluation_results.csv"

    @property
    def defect_log_csv(self) -> Path:
        return self.data_dir / "defect_log.csv"

    @property
    def run_manifest_json(self) -> Path:
        return self.data_dir / "run_manifest.json"

    @property
    def clinical_report_md(self) -> Path:
        return self.reports_dir / "clinical_llm_safety_report.md"

    @property
    def legacy_report_md(self) -> Path:
        return self.reports_dir / "evaluation_report.md"


def default_paths() -> EvaluationPaths:
    """Paths for a normal install: package lives in src/clinical_llm_safety_eval/."""
    project_root = Path(__file__).resolve().parents[2]
    return EvaluationPaths(project_root=project_root)
