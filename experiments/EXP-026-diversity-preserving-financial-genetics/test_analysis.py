import importlib.util
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("exp026", HERE / "analysis.py")
M = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def population():
    rng = np.random.default_rng(1)
    return [M.B.draw_genome(rng) for _ in range(12)]


def test_candidate_budgets_and_hybrid_composition():
    pop = population()
    for method in M.METHODS:
        candidates, origins = M.generate_candidates(method, pop, np.random.default_rng(2))
        assert len(candidates) == 48
        if method.startswith("hybrid"):
            assert origins.count("child") == 36
            assert origins.count("immigrant") == 12


def test_family_paths_are_deterministic_and_distinct():
    a = M.simulate_family(7, "rotation")
    b = M.simulate_family(7, "rotation")
    c = M.simulate_family(7, "mean_reversion")
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_signature_uses_only_past():
    returns = M.simulate_family(9, "correlation_flip")
    genome = population()[0]
    original = M.phenotype_signature(genome, returns, 300)
    altered = returns.copy()
    altered[300:] = 999
    assert np.allclose(original, M.phenotype_signature(genome, altered, 300))


def test_diversity_reserve_respects_fitness_floor():
    returns = M.simulate_family(10, "rotation")
    pop = population()
    candidates, _ = M.generate_candidates("hybrid_diverse", pop, np.random.default_rng(4))
    selected, margin = M.select_diverse(pop + candidates, returns, 252)
    assert len(selected) == 12
    assert margin >= -1e-12

