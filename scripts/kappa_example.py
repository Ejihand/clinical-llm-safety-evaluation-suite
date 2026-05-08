#!/usr/bin/env python3
"""
Tiny Cohen's kappa example between two reviewer columns (status labels).

Usage (from repo root after pip install -e .):

  python scripts/kappa_example.py path/to/reviews.csv reviewer_a_status reviewer_b_status

The CSV must have a header row. Status values are treated as strings (for example
Pass, Review, Fail).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from clinical_llm_safety_eval.kappa_stats import cohen_kappa


def main() -> None:
    if len(sys.argv) != 4:
        print(__doc__.strip())
        sys.exit(1)

    path = Path(sys.argv[1])
    col_a = sys.argv[2]
    col_b = sys.argv[3]

    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    a = [r[col_a].strip() for r in rows]
    b = [r[col_b].strip() for r in rows]
    agree = sum(1 for x, y in zip(a, b) if x == y)

    print(f"Rows: {len(a)}")
    print(f"Percent agreement: {100.0 * agree / len(a):.1f}%")
    print(f"Cohen kappa: {cohen_kappa(a, b):.3f}")


if __name__ == "__main__":
    main()
