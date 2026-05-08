# Human evaluation and agreement

Automation in this repo is a **first pass**. Clinical AI programs still rely on
trained reviewers for edge cases, policy, and accountability.

## When to use two human reviewers

- High-stakes categories (emergencies, pediatrics, pregnancy, mental health).
- Any case flagged **Fail** or **Review** by automation.
- A change in model version, system prompt, or safety policy (spot check).

## Simple agreement metrics

1. **Percent agreement** on a coarse label: both reviewers assign the same
   `status` (`Pass` / `Review` / `Fail`) to a case.
2. **Cohen's kappa** on the same labels: corrects for chance agreement when
   categories are imbalanced. Values near 1 mean strong agreement; values near
   or below 0 mean agreement is not much better than random for that prevalence.

## Disagreement policy (example)

1. If reviewers disagree on **Fail vs Pass**, escalate to an adjudicator
   (clinical lead or safety owner).
2. Record the resolution in the defect or ticket; update rubric notes if the
   scorer missed a pattern.

## Synthetic template

Use `templates/human_review_template.csv`. It mirrors the rubric dimensions and
stores the automation label side-by-side for quick calibration studies.

See `scripts/kappa_example.py` (uses `clinical_llm_safety_eval.kappa_stats`).
