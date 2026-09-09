"""Small exact-table utilities for exploratory feasibility summaries."""

from __future__ import annotations

from math import comb, inf


def odds_ratio(table: tuple[tuple[int, int], tuple[int, int]]) -> float:
    (a, b), (c, d) = table
    if min(a, b, c, d) < 0:
        raise ValueError("counts must be non-negative")
    denominator = b * c
    if denominator == 0:
        return inf if a * d > 0 else float("nan")
    return (a * d) / denominator


def fisher_exact_two_sided(
    table: tuple[tuple[int, int], tuple[int, int]],
) -> float:
    """Return the probability-ordering two-sided Fisher exact p-value."""
    (a, b), (c, d) = table
    if min(a, b, c, d) < 0:
        raise ValueError("counts must be non-negative")
    row_one = a + b
    column_one = a + c
    total = a + b + c + d
    if total == 0:
        raise ValueError("table must contain observations")

    denominator = comb(total, row_one)

    def probability(x: int) -> float:
        return comb(column_one, x) * comb(total - column_one, row_one - x) / denominator

    lower = max(0, row_one - (total - column_one))
    upper = min(row_one, column_one)
    observed = probability(a)
    return min(
        1.0,
        sum(
            probability(x)
            for x in range(lower, upper + 1)
            if probability(x) <= observed + 1e-15
        ),
    )
