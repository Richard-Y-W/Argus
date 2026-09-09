import pytest

from .contingency import fisher_exact_two_sided, odds_ratio


def test_odds_ratio() -> None:
    assert odds_ratio(((4, 12), (3, 5))) == pytest.approx(5 / 9)


def test_fisher_exact_is_one_for_balanced_table() -> None:
    assert fisher_exact_two_sided(((5, 5), (5, 5))) == pytest.approx(1.0)


def test_hwang_probe_fisher_exact_value() -> None:
    assert fisher_exact_two_sided(((4, 12), (3, 5))) == pytest.approx(
        0.6466264475417794
    )


def test_fisher_exact_rejects_empty_table() -> None:
    with pytest.raises(ValueError, match="observations"):
        fisher_exact_two_sided(((0, 0), (0, 0)))


def test_negative_counts_are_rejected() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        fisher_exact_two_sided(((-1, 2), (3, 4)))
