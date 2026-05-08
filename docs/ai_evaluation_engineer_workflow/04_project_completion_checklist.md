# Project Completion Checklist

This checklist describes what I would confirm before closing a clinical LLM
evaluation project.

## Scope and Planning

- [ ] Intended use is documented.
- [ ] Out-of-scope uses are documented.
- [ ] Target users are defined.
- [ ] Risk assumptions are documented.
- [ ] Evaluation categories are agreed.
- [ ] Pass/fail or risk rating approach is documented.

## Test Design

- [ ] Test cases cover high-risk clinical scenarios.
- [ ] Test cases include expected safe behavior.
- [ ] Test cases include unsafe failure modes.
- [ ] Test cases include tags for traceability.
- [ ] High-risk prompts are represented.
- [ ] Unsafe request/refusal cases are represented.

## Execution

- [ ] Model responses are collected.
- [ ] Model/system version is recorded if available.
- [ ] Evaluator runs successfully.
- [ ] Evaluation results are generated.
- [ ] Defect log is generated.
- [ ] Report is generated.
- [ ] Tests pass.

## Defect Review

- [ ] Critical defects are manually reviewed.
- [ ] High defects are manually reviewed.
- [ ] Review-status cases are triaged.
- [ ] Failure types are confirmed.
- [ ] Severity levels are confirmed.
- [ ] Recommendations are documented.
- [ ] Regression cases are identified.

## Reporting

- [ ] Executive summary is clear.
- [ ] Evaluation scope is clear.
- [ ] Test dataset summary is included.
- [ ] Key metrics are included.
- [ ] Critical/high-risk failures are listed.
- [ ] Defect summary is included.
- [ ] Limitations are included.
- [ ] Recommendations are included.
- [ ] Final risk rating is included.

## Closure Decision

Choose one:

- [ ] Safe to proceed for intended use.
- [ ] Proceed with limitations.
- [x] Mitigation required before release.
- [ ] Not recommended for deployment.

Reason:

Critical missed-escalation and unsafe medication/refusal failures were detected
in the sample response set.

## Final Artifacts

- [x] `evaluation_plan.md`
- [x] `rubric.md`
- [x] `data/test_cases.csv`
- [x] `data/model_responses.csv`
- [x] `data/evaluation_results.csv`
- [x] `data/defect_log.csv`
- [x] `reports/clinical_llm_safety_report.md`
- [x] `tests/test_scoring.py`
