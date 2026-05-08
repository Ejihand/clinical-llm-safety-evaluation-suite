"""Smoke test for Cohen kappa helper in scripts/kappa_example.py."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from clinical_llm_safety_eval.kappa_stats import cohen_kappa


@pytest.fixture
def sample_reviews(tmp_path: Path) -> Path:
    path = tmp_path / "reviews.csv"
    rows = [
        {"case_id": "1", "r1": "Pass", "r2": "Pass"},
        {"case_id": "2", "r1": "Fail", "r2": "Fail"},
        {"case_id": "3", "r1": "Review", "r2": "Pass"},
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["case_id", "r1", "r2"])
        w.writeheader()
        w.writerows(rows)
    return path


def test_cohen_kappa_on_perfect_agreement():
    labels = ["Pass", "Pass", "Fail"]
    assert pytest.approx(cohen_kappa(labels, labels), rel=1e-6) == 1.0


def test_cohen_kappa_reads_fixture_rows(sample_reviews: Path) -> None:
    with sample_reviews.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    a = [r["r1"] for r in rows]
    b = [r["r2"] for r in rows]
    kappa = cohen_kappa(a, b)
    assert -0.5 <= kappa <= 1.0
