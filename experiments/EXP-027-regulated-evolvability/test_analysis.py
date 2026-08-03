import importlib.util
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("exp027", HERE / "analysis.py")
M = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def population():
    rng = np.random.default_rng(3)
    return [M.B.draw_genome(rng) for _ in range(12)]


def test_routes_at_registered_thresholds():
    assert M.route(1.249) == "evolution"
    assert M.route(1.25) == "hybrid_quality"
    assert M.route(2.499) == "hybrid_quality"
    assert M.route(2.50) == "random"


def test_distance_is_causal_and_finite():
    returns = M.simulate_family(5, "moderate_rotation")
    original = M.environmental_distance(returns, 300)
    altered = returns.copy()
    altered[300:] = 999
    assert np.isfinite(original)
    assert original == M.environmental_distance(altered, 300)
    constant = np.zeros_like(returns)
    assert np.isfinite(M.environmental_distance(constant, 300))


def test_families_deterministic_and_distinct():
    a = M.simulate_family(8, "small_drift")
    b = M.simulate_family(8, "small_drift")
    c = M.simulate_family(8, "correlation_break")
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_equal_candidate_budget_and_hybrid_composition():
    returns = M.simulate_family(9, "small_drift")
    pop = population()
    rng = np.random.default_rng(10)
    for method in M.METHODS:
        candidates, _, _ = M.generate(method, pop, rng, returns, 300)
        assert len(candidates) == 48
    candidates, origins = M.E.generate_candidates("hybrid_quality", pop, np.random.default_rng(11))
    assert len(candidates) == 48
    assert origins.count("child") == 36 and origins.count("immigrant") == 12

