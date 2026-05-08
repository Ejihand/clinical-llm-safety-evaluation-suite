# AI Evaluation Engineer Workflow

This folder documents how I would approach this project if I were employed as an
AI Evaluation Engineer and assigned to evaluate a clinical LLM.

The goal is to show the full evaluation lifecycle:

1. Understanding the model and intended use.
2. Planning a risk-based evaluation.
3. Designing clinical test cases.
4. Executing the evaluation.
5. Logging defects.
6. Analyzing safety risk.
7. Reporting findings.
8. Closing the project with recommendations and next steps.

This process is intentionally QA-oriented. It treats the LLM as a system under
test and evaluates its outputs against expected safe behavior, known failure
modes, and clinical risk assumptions.

## Files in This Folder

- `01_evaluation_lifecycle.md`: end-to-end process from idea to completion.
- `02_workplace_execution_plan.md`: how I would run this as an employed AI Evaluation Engineer.
- `03_defect_review_process.md`: how I would classify, review, and communicate defects.
- `04_project_completion_checklist.md`: final sign-off checklist before project closure.

## Positioning

This documentation is written from the perspective of a Medical Laboratory
Scientist, Manual QA professional, and MSc Bioinformatics student transitioning
into Clinical AI Evaluation Engineering.

It emphasizes:

- risk-based testing
- structured test design
- expected versus actual behavior
- defect severity classification
- clinical safety thinking
- regression-style evaluation
- clear stakeholder reporting
