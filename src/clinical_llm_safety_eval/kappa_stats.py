"""Lightweight agreement statistics (stdlib-friendly)."""

from __future__ import annotations

from collections import Counter


def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> float:
    """Compute Cohen's kappa for two raters (same length, categorical labels)."""
    n = len(labels_a)
    if n == 0 or len(labels_b) != n:
        raise ValueError("Both reviewers must rate the same number of items.")

    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    p_o = agree / n

    cat_a = Counter(labels_a)
    cat_b = Counter(labels_b)
    categories = sorted(set(labels_a) | set(labels_b))
    p_e = sum((cat_a[c] / n) * (cat_b[c] / n) for c in categories)

    if p_e >= 1.0:
        return 1.0 if p_o == 1.0 else 0.0
    return (p_o - p_e) / (1.0 - p_e)
