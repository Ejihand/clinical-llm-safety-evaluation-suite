# Evaluation Lifecycle: From Idea to Project Completion

This document describes how I would evaluate a clinical LLM from the first idea
through planning, execution, reporting, and closure.

## 1. Understand the Assignment

If I were given a clinical LLM to evaluate, I would first clarify what the model
is supposed to do and what it must not do.

Key questions:

- What is the intended use of the model?
- Who will use it: patients, clinicians, support staff, researchers, or QA reviewers?
- Is it patient-facing or internal-facing?
- Is it expected to answer general health questions, interpret lab results, triage symptoms, or summarize records?
- What clinical areas are in scope?
- What clinical areas are out of scope?
- What are the unacceptable failure modes?

For this project, I assume the model is a patient-facing informational assistant
that may answer clinical questions but must not diagnose, prescribe, replace
emergency care, or provide unsafe personalized treatment instructions.

## 2. Define the Evaluation Objective

Objective:

Evaluate whether the clinical LLM produces safe, cautious, and reliable
responses to patient-facing prompts across high-risk and medium-risk clinical
scenarios.

The evaluation focuses on:

- safety
- medical accuracy
- escalation appropriateness
- medical caution
- completeness
- clarity
- hallucination or unsupported claim risk
- overconfidence risk
- refusal behavior for unsafe requests

## 3. Identify Risks and Failure Modes

Before creating test cases, I would list the highest-risk ways the model could
fail.

Examples:

- Misses chest pain, stroke, sepsis, or pediatric emergency red flags.
- Provides unsafe medication advice.
- Normalizes dangerous laboratory results.
- Gives overconfident diagnoses from limited context.
- Fails to refuse unsafe dosing requests.
- Gives generic reassurance during mental health crisis.
- Encourages delayed care when urgent care is needed.

This risk analysis drives the test design.

## 4. Create an Evaluation Plan

The evaluation plan defines the rules of the project before execution begins.

It should include:

- objective
- intended use
- out-of-scope uses
- target users
- risk assumptions
- evaluation categories
- test case design approach
- scoring approach
- defect classification
- pass/fail criteria
- deliverables

In this project, that plan is documented in `evaluation_plan.md`.

## 5. Design Test Cases

I would design test cases like a QA analyst designs test scenarios: each case
should test a specific risk.

Each test case should include:

- case ID
- category
- risk level
- prompt
- expected safe behavior
- unsafe failure modes
- tags

The test set should include both common and high-risk cases. In clinical AI
evaluation, rare but dangerous failures matter.

## 6. Collect or Generate Model Responses

Next, I would collect the model's responses to each test prompt.

In a workplace setting, this might involve:

- running prompts through a model endpoint
- saving raw outputs
- preserving model version and prompt configuration
- recording date of evaluation
- documenting any system prompt or safety layer used

In this portfolio project, sample model responses are stored in
`data/model_responses.csv`.

The sample response set intentionally includes safe, incomplete, unsafe,
overconfident, missed-escalation, and refusal-failure examples.

## 7. Execute the Evaluation

Execution should be reproducible.

```bash
python -m clinical_llm_safety_eval.evaluator
```

The evaluator:

- reads test cases
- reads model responses
- scores each response
- flags high-risk failures
- assigns case status
- generates `data/evaluation_results.csv`
- generates `data/defect_log.csv`
- prints a terminal summary

## 8. Review Defects

After automated scoring, I would review the defect log manually.

For each defect, I would ask:

- What was expected?
- What did the model actually say?
- What patient safety risk does this create?
- Is the severity correct?
- Is this a one-off failure or a pattern?
- Should this become a regression test?
- What mitigation is recommended?

Clinical LLM evaluation should not stop at a score. The defect analysis is where
the safety meaning becomes clear.

## 9. Analyze Patterns

I would look for repeated failure patterns across categories.

Examples:

- repeated missed escalation in emergency prompts
- overconfidence in lab interpretation
- unsafe medication advice
- weak refusal behavior for dosing requests
- poor handling of pediatric or pregnancy scenarios

Pattern analysis helps decide whether the model needs a prompt fix, safety
policy change, retrieval improvement, model change, or stricter deployment
limits.

## 10. Generate the Report

```bash
python -m clinical_llm_safety_eval.report_generator
```

The report summarizes:

- executive summary
- model/system evaluated
- evaluation scope
- test dataset summary
- methods
- key metrics
- critical/high-risk failures
- defect summary
- clinical safety findings
- limitations
- recommendations
- final risk rating

## 11. Communicate Findings

As an AI Evaluation Engineer, I would communicate findings in a way that is
useful to technical, clinical, and product stakeholders.

I would avoid vague statements like:

- "The model is bad."
- "The model needs improvement."

Instead, I would say:

- "The model missed emergency escalation in stroke-like symptoms."
- "The model provided unsafe medication discontinuation advice."
- "The model failed refusal behavior for a personalized insulin dosing request."
- "These failures should block patient-facing release until mitigated and retested."

## 12. Close the Project

Project completion should include:

- final report generated
- defect log reviewed
- high-risk failures clearly identified
- recommendations documented
- limitations documented
- next-step regression tests identified
- final risk rating assigned

The project is complete only when the findings can support a decision:

- safe to proceed
- proceed with limitations
- requires mitigation and retesting
- not recommended for intended use

For the current sample response set, the final risk rating is **High**, meaning
the model/system would require mitigation and regression testing before use in a
patient-facing clinical information workflow.
