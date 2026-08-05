import importlib.util
from pathlib import Path

import numpy as np


SPEC = importlib.util.spec_from_file_location("exp030", Path(__file__).with_name("analysis.py"))
analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(analysis)


def test_metrics_and_reduction_move_health_in_right_direction() -> None:
    exposure = np.full(6, 40.0)
    before = analysis.metrics(exposure, 100.0, 32.0, np.ones(6))
    new, equity, buffer, total = analysis.reduce(exposure, np.full(6, 5.0), 100.0, 32.0, 1.0)
    after = analysis.metrics(new, equity, buffer, np.ones(6))
    assert total == 30.0
    assert after[0] < before[0]
    assert after[1] > before[1]


def test_return_paths_are_shared_across_policies_and_deterministic() -> None:
    first = analysis.return_path("combined", 30001)
    second = analysis.return_path("combined", 30001)
    other = analysis.return_path("combined", 30002)
    assert np.array_equal(first, second)
    assert not np.array_equal(first, other)


def test_immune_has_no_hidden_family_argument() -> None:
    exposure = np.full(6, 40.0)
    multipliers = np.array([5.0, 1, 1, 1, 1, 1])
    result = analysis.immune_action(exposure, 100.0, 20.0, multipliers, np.zeros(6), 1.0)
    reductions = result[3]
    assert reductions[0] > 0
    assert result[0].sum() < exposure.sum()


def test_benign_family_is_explicit() -> None:
    state = analysis.family_state("benign_volatility", 40)
    assert np.allclose(state[5], 1.0)
    assert state[6] == set()

