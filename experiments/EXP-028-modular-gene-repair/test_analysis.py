import importlib.util
from pathlib import Path

import numpy as np


PATH = Path(__file__).with_name("analysis.py")
SPEC = importlib.util.spec_from_file_location("exp028_analysis", PATH)
analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(analysis)


def test_damage_localization_and_candidate_budget() -> None:
    rng = np.random.default_rng(7)
    train = rng.normal(0, 0.01, size=(252, 5))
    train[-63:, 3] += 0.02
    incumbent = np.full(5, 0.2)
    candidates = analysis.stochastic_weights("localized", train, incumbent, 10)
    assert candidates.shape == (64, 5)
    assert np.allclose(candidates.sum(axis=1), 1.0)
    assert 3 in np.argsort(analysis.damage_scores(train))[-2:]
    unchanged = set(range(5)) - set(np.argsort(analysis.damage_scores(train))[-2:])
    assert np.allclose(candidates[:, list(unchanged)], 0.2)


def test_equal_stochastic_budgets_and_determinism() -> None:
    rng = np.random.default_rng(9)
    train = rng.normal(0, 0.01, size=(252, 5))
    incumbent = np.full(5, 0.2)
    for method in ("localized", "all_gene", "random"):
        first = analysis.stochastic_weights(method, train, incumbent, 22)
        second = analysis.stochastic_weights(method, train, incumbent, 22)
        assert len(first) == 64
        assert np.array_equal(first, second)


def test_loader_uses_daily_value_weighted_block() -> None:
    frame = analysis.load_french_zip(analysis.RAW / "archive_202412.zip")
    assert list(frame.columns) == ["Cnsmr", "Manuf", "HiTec", "Hlth", "Other"]
    assert frame.index.is_monotonic_increasing
    assert frame.index.max().year == 2024
    assert frame.abs().max().max() < 1.0

