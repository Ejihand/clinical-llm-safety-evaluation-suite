# Clinical LLM Safety Evaluation Suite

[![CI](https://github.com/YOUR_GITHUB_USER/YOUR_REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USER/YOUR_REPO/actions/workflows/ci.yml)

**A QA-style evaluation framework for assessing clinical LLM responses for
safety, escalation, hallucination risk, overconfidence, and patient-facing
reliability.**

This is a Clinical AI Evaluation Engineer portfolio project. It does not build a
clinical chatbot. It provides a **versioned clinical safety test pack**,
**deterministic rule-based triage scoring**, **run manifests for reproducibility**,
and artifacts (CSV results, defect log, Markdown reports) designed to pair with
**human review** or with **batch / API-generated** model outputs.

## Project Overview

Clinical LLMs can produce responses that are fluent, confident, and unsafe at
the same time. This project evaluates sample model responses to patient-facing
clinical prompts and asks a practical QA question:

> Would this response be safe, cautious, and reliable enough for a patient-facing
> informational workflow?

The suite uses CSV-based test cases, sample model responses, a transparent
rubric, an automated evaluator, a generated defect log, and a professional
Markdown report.

## What Problem This Project Solves

Many AI demos focus on generating answers. Clinical AI evaluation requires a
different mindset: defining expected behavior, testing risky edge cases,
identifying failure modes, classifying defects, and turning findings into
actionable risk decisions.

This project demonstrates how QA concepts can be applied to clinical LLM
evaluation:

- Test case design.
- Risk-based testing.
- Expected versus actual behavior.
- Defect severity classification.
- Regression-style failure tracking.
- Structured evaluation reporting.

## Intended Use of the Evaluated Model

The evaluated model is assumed to be a general-purpose LLM answering
patient-facing health questions in an informational setting.

The expected model behavior is to:

- Identify emergency red flags.
- Recommend appropriate escalation.
- Avoid unsupported diagnoses.
- Use cautious, non-overconfident language.
- Refuse unsafe personalized medication or treatment instructions.
- Encourage clinician review when clinical context is incomplete.

## Why Clinical LLM Evaluation Matters

Clinical AI systems should not be evaluated only for helpfulness or grammar.
Safety-focused evaluation asks:

- Did the model miss an emergency?
- Did it provide unsafe medication advice?
- Did it overstate certainty?
- Did it hallucinate a diagnosis or treatment?
- Did it fail to refuse an unsafe request?
- Did it communicate in a way a patient could act on safely?

These questions are especially important in domains such as lab result
interpretation, medication safety, pediatric red flags, pregnancy medication
safety, CKD, diabetes, infectious disease, and mental health crisis response.

## Portfolio Context

This project reflects a transition from Manual QA and healthcare laboratory
science into Clinical AI Evaluation / AI Evaluation Engineering. It combines:

- Medical Laboratory Science knowledge.
- Manual QA thinking.
- Bioinformatics-oriented data handling.
- Python scripting.
- Clinical safety evaluation.

The emphasis is on evaluating model behavior, not building a patient-facing
medical product.

The folder `docs/ai_evaluation_engineer_workflow/` documents how I would handle
this kind of evaluation in a workplace setting, from intake and planning through
execution, defect review, reporting, and project closure.

## Project Structure

```text
clinical-llm-safety-evaluation-suite/
  README.md
  pyproject.toml
  LICENSE
  CHANGELOG.md
  evaluation_plan.md
  rubric.md
  requirements.txt / requirements-lock.txt
  .github/workflows/ci.yml
  data/
    test_cases.csv
    model_responses.csv
    model_responses_run_b.csv   # example alternate response set
    evaluation_results.csv
    defect_log.csv
    run_manifest.json
  src/clinical_llm_safety_eval/
    scoring.py
    evaluator.py
    report_generator.py
    manifest.py
    compare_runs.py
    model_runner.py
    ...
  tests/
    ...
  templates/
    human_review_template.csv
  scripts/
    kappa_example.py
  reports/
    clinical_llm_safety_report.md
    run_comparison.md
  docs/
    calibration.md
    human_evaluation_agreement.md
    big_health_system_onboarding_playbook.md
    ai_evaluation_engineer_workflow/
```

## Evaluation Workflow

1. Define clinical safety test cases in `data/test_cases.csv`.
2. Add model responses in `data/model_responses.csv`.
3. Run the evaluator.
4. Score each response across the rubric.
5. Flag high-risk failures.
6. Generate `data/evaluation_results.csv`.
7. Generate `data/defect_log.csv`.
8. Generate `data/run_manifest.json` (versions, input hashes, git metadata).
9. Generate `reports/clinical_llm_safety_report.md`.

## Test Dataset Design

The dataset contains **25** clinical test cases (including a few adversarial rows
documented in [docs/calibration.md](docs/calibration.md)) across:

- Emergency symptoms.
- Medication safety.
- Lab result interpretation.
- CKD-related lab interpretation.
- Pregnancy medication safety.
- Pediatric red flags.
- Mental health crisis.
- Overdiagnosis risk.
- Diabetes result interpretation.
- Infectious disease red flags.

Each test case includes:

- `case_id`
- `category`
- `risk_level`
- `prompt`
- `expected_safe_behavior`
- `unsafe_failure_modes`
- `tags`

The sample model responses intentionally include safe, incomplete, unsafe,
overconfident, and missed-escalation examples. This makes the evaluator useful
as a failure-detection demo rather than a set of only successful cases.

## Scoring Rubric Summary

Each response is scored from 1 to 5 across:

- Safety.
- Medical accuracy.
- Escalation appropriateness.
- Medical caution.
- Completeness.
- Clarity.
- Hallucination or unsupported claim risk.
- Overconfidence risk.
- Refusal behavior for unsafe requests.

See [rubric.md](rubric.md) for the full rubric.

## Defect Classification

The evaluator creates a QA-style defect log with:

- Defect ID.
- Case ID.
- Severity.
- Failure type.
- Expected behavior.
- Actual behavior.
- Risk explanation.
- Recommendation.
- Status.

Severity levels are:

- Critical.
- High.
- Medium.
- Low.

## Sample Results

Current sample run (baseline `data/model_responses.csv`, regenerate locally):

```text
Cases evaluated: 25
Overall average score: 3.85/5
High-risk failures flagged: 9
Defects logged: 14

Case status counts:
Pass      11
Fail       9
Review     5
```

Final report risk rating:

```text
High
```

The report is available at:

```text
reports/clinical_llm_safety_report.md
```

## Installation

From the repository root, use a virtual environment and install the package in
editable mode (recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Optional API batching for `model_runner` (OpenAI-compatible):

```bash
pip install -e ".[model]"
```

For a more reproducible dependency set, see [requirements-lock.txt](requirements-lock.txt).

## How to Run the Project

Run the evaluator (writes results, defect log, and `data/run_manifest.json`):

```bash
python -m clinical_llm_safety_eval.evaluator
```

Alternate response file and outputs (for A/B or regression demos):

```bash
python -m clinical_llm_safety_eval.evaluator \
  --responses-csv model_responses_run_b.csv \
  --results-csv evaluation_results_run_b.csv \
  --defect-log-csv defect_log_run_b.csv \
  --manifest-json run_manifest_run_b.json \
  --model-id demo-model-b \
  --temperature 0.2
```

Generate the report:

```bash
python -m clinical_llm_safety_eval.report_generator
```

Compare two result CSVs:

```bash
python -m clinical_llm_safety_eval.compare_runs \
  --a data/evaluation_results.csv \
  --b data/evaluation_results_run_b.csv \
  --out reports/run_comparison.md \
  --label-a baseline \
  --label-b run_b
```

Optional: build `model_responses.csv` from prompts (`--dry-run` needs no API key):

```bash
python -m clinical_llm_safety_eval.model_runner \
  --test-cases data/test_cases.csv \
  --output data/model_responses_new.csv \
  --dry-run
```

With `OPENAI_API_KEY` set and `pip install -e ".[model]"`, omit `--dry-run` to
call the API (see module docstring for env vars).

Run tests:

```bash
python -m pytest tests -q
```

If Windows blocks pytest cache creation in a synced folder:

```bash
python -m pytest tests -q -p no:cacheprovider
```

## Reproducibility and human review

- **Run manifest**: each evaluation writes `data/run_manifest.json` with
  `test_pack_version`, `rubric_version`, input SHA-256 hashes, and git metadata
  when available. The Markdown report includes a short manifest footer.
- **Calibration**: read [docs/calibration.md](docs/calibration.md) for known
  automation limits (including adversarial rows TC023–TC025).
- **Human labels**: use [templates/human_review_template.csv](templates/human_review_template.csv)
  and [docs/human_evaluation_agreement.md](docs/human_evaluation_agreement.md).
  Cohen’s kappa helper: `clinical_llm_safety_eval.kappa_stats` and
  `scripts/kappa_example.py`.

## Data governance

- **Synthetic demo data only** — no real patient PHI in this repository.
- **Local retention** by default; do not paste real clinical data into public repos.
- **Not for clinical decisions** — automation triages outputs; clinicians and
  policy owners own release choices. See `evaluation_plan.md` SaMD scope note.

## Main Outputs

- `data/evaluation_results.csv`: per-case rubric scores and status.
- `data/defect_log.csv`: QA-style defect log.
- `data/run_manifest.json`: reproducibility metadata for the run.
- `reports/clinical_llm_safety_report.md`: professional evaluation report.
- `reports/run_comparison.md`: example A/B comparison (after you run `compare_runs`).

## Limitations

This is a portfolio and learning project, not a medical device or clinical
decision support system.

Current limitations:

- The scoring is rule-based and keyword-driven (see [docs/calibration.md](docs/calibration.md)).
- The dataset is synthetic and small — no real PHI.
- Live model calls are optional; default fixtures use CSV only.
- Automated scores are not clinician reviewer labels.
- It does not verify citations or guideline adherence.
- It should not be used to make clinical decisions.

## Future Improvements

- Add more test cases across specialties and demographics.
- Add charts for defect severity and rubric category trends.
- Add severity weighting for final risk rating.
- Add regression test snapshots committed per rubric version.
- Build a Streamlit dashboard for reviewers.

## Skills Demonstrated

- Clinical AI safety evaluation.
- QA-style test design.
- Risk-based testing.
- Defect classification.
- Expected versus actual behavior analysis.
- Medical laboratory and clinical risk reasoning.
- Python scripting.
- CSV data handling with pandas.
- Markdown report generation.
- Pytest-based unit and integration tests.
- Continuous integration workflow.
- Professional technical documentation.

## Portfolio Positioning

This project is positioned for Clinical AI Evaluation Engineer, AI Safety
Evaluator, Healthcare AI QA Analyst, or AI Model Evaluation roles. It shows that
clinical AI evaluation is not just about asking a model questions. It requires
structured test design, safety-oriented judgment, defect logging, risk rating,
and clear communication of limitations.

## Disclaimer

This project is for education and portfolio demonstration only. It does not
provide medical advice and should not be used to make clinical decisions.
# clinical-llm-safety-evaluation-suite
