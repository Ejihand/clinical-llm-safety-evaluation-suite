# Calibration: what the automation gets wrong

This project uses transparent, keyword-style checks. Those checks are useful for
**triage and regression testing**, but they are **not** a clinical gold standard.

## Known blind spots

1. **Paraphrased safe care**  
   A response can be clinically appropriate while sharing few long words with
   `expected_safe_behavior`. The `completeness` score uses word overlap and may
   mark good answers as weak.

2. **Unsafe phrasing that evades lists**  
   Some harmful instructions may not match phrases in `UNSAFE_ACTION_TERMS`.
   Example pattern: “double your usual dose” instead of “double your dose.”
   Adversarial case TC025 illustrates this class of gap.

3. **Missed escalation without emergency keywords**  
   A model can recommend delay (for example “see someone in a few weeks”) for
   symptoms that need faster care, without using words like “emergency.” TC023 is
   written to expose that the automation may not always downgrade those answers
   as harshly as a clinician would.

4. **False comfort from cautious tone**  
   Phrases such as “contact a clinician” can raise scores even when timing is
   still unsafe in real practice. Human review is required.

## When to override automation

- Any case where a clinician disagrees with the **Pass** label.
- Any **pediatric**, **pregnancy**, **anticoagulation**, or **crisis** scenario,
  even if the score looks fine.
- Any deployment where the product owner changes model or prompt version:
  rerun the pack, compare manifests, and sample human review.

## How this is used in hiring conversations

Senior eval engineers are expected to say: **automation compresses the search
space; humans own the decision on patient harm.** This file documents that line
explicitly for reviewers and interviewers.
