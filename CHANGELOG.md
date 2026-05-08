# Changelog

All notable changes to this evaluation harness and test pack are recorded here.

## Evaluation artifacts

- **test_pack_version** (see `run_manifest.json` / `evaluation_version.py`): bump when
  `data/test_cases.csv` or fixed response fixtures change.
- **rubric_version**: bump when `src/clinical_llm_safety_eval/scoring.py` logic changes.
- **harness_version**: the Python package version in `pyproject.toml`.

## [1.1.0] test pack

- Added adversarial cases TC023–TC025 for calibration demos.
- Added `data/model_responses_run_b.csv` for A/B comparison examples.

## [1.0.0] harness

- Packaged as `clinical-llm-safety-eval` with run manifests, CI, and integration tests.
- Rule-based scoring unchanged from the original portfolio baseline (rubric v1.0.0).
