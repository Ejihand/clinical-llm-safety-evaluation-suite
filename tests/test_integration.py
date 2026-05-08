"""End-to-end evaluation and report checks on tiny fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from shutil import copyfile

import pandas as pd
import pytest

from clinical_llm_safety_eval.evaluator import load_inputs, run
from clinical_llm_safety_eval.paths import EvaluationPaths
from clinical_llm_safety_eval.report_generator import build_report
from clinical_llm_safety_eval.scoring import RUBRIC_CATEGORIES


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "minimal"


def _seed_minimal_project(target: Path) -> EvaluationPaths:
    data = target / "data"
    data.mkdir(parents=True)
    copyfile(FIXTURE_DIR / "test_cases.csv", data / "test_cases.csv")
    copyfile(FIXTURE_DIR / "model_responses.csv", data / "model_responses.csv")
    return EvaluationPaths(project_root=target)


def test_load_inputs_rejects_missing_responses(tmp_path: Path) -> None:
    paths = _seed_minimal_project(tmp_path)
    # overwrite with incomplete responses
    copyfile(FIXTURE_DIR / "model_responses_missing_one.csv", paths.data_dir / "model_responses.csv")
    with pytest.raises(ValueError, match="do not have a model response"):
        load_inputs(paths, paths.data_dir / "model_responses.csv")


def test_run_writes_csvs_and_manifest(tmp_path: Path) -> None:
    paths = _seed_minimal_project(tmp_path)
    results_path = paths.data_dir / "evaluation_results.csv"
    defect_path = paths.data_dir / "defect_log.csv"
    manifest_path = paths.data_dir / "run_manifest.json"

    results, defect_log, manifest = run(
        paths,
        responses_csv=paths.data_dir / "model_responses.csv",
        results_csv=results_path,
        defect_log_csv=defect_path,
        manifest_json=manifest_path,
    )

    assert len(results) == 3
    assert manifest_path.exists()
    assert "run_id" in manifest
    assert "test_pack_version" in manifest
    for col in RUBRIC_CATEGORIES:
        assert col in results.columns
    assert "case_status" in results.columns
    assert results_path.exists()
    assert defect_path.exists()


def test_report_contains_manifest_footer(tmp_path: Path) -> None:
    paths = _seed_minimal_project(tmp_path)
    run(
        paths,
        responses_csv=paths.data_dir / "model_responses.csv",
        results_csv=paths.data_dir / "evaluation_results.csv",
        defect_log_csv=paths.data_dir / "defect_log.csv",
        manifest_json=paths.data_dir / "run_manifest.json",
    )
    manifest = json.loads((paths.data_dir / "run_manifest.json").read_text(encoding="utf-8"))
    results = pd.read_csv(paths.data_dir / "evaluation_results.csv")
    defect_log = pd.read_csv(paths.data_dir / "defect_log.csv")
    md = build_report(results, defect_log, manifest=manifest)
    assert "Run manifest" in md
    assert manifest["run_id"] in md
