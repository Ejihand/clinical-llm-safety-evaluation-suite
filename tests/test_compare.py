"""Tests for evaluation run comparison."""

from __future__ import annotations

import io

import pandas as pd

from clinical_llm_safety_eval.compare_runs import compare_dataframes


def test_compare_detects_regression() -> None:
    a = pd.DataFrame(
        [
            {"case_id": "C1", "overall_score": 4.5, "case_status": "Pass", "high_risk_failure": False, "safety": 5, "escalation": 5, "refusal_behavior": 5, "medical_accuracy": 4},
            {"case_id": "C2", "overall_score": 4.0, "case_status": "Pass", "high_risk_failure": False, "safety": 4, "escalation": 4, "refusal_behavior": 5, "medical_accuracy": 4},
        ]
    )
    b = pd.DataFrame(
        [
            {"case_id": "C1", "overall_score": 4.5, "case_status": "Pass", "high_risk_failure": False, "safety": 5, "escalation": 5, "refusal_behavior": 5, "medical_accuracy": 4},
            {"case_id": "C2", "overall_score": 2.5, "case_status": "Fail", "high_risk_failure": True, "safety": 1, "escalation": 1, "refusal_behavior": 1, "medical_accuracy": 2},
        ]
    )
    md = compare_dataframes(a, b, "A", "B")
    assert "C2" in md
    assert "Regression" in md
