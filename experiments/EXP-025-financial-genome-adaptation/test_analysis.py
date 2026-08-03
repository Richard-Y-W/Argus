import importlib.util
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("exp025", HERE / "analysis.py")
M = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def test_mutation_changes_only_one_gene_and_stays_bounded():
    parent = M.Genome(80, 40, 0.10, 0.60, 0.10)
    rng = np.random.default_rng(7)
    for _ in range(200):
        child, selected = M.mutate(parent, rng)
        changed = [k for k in M.GENES if getattr(child, k) != getattr(parent, k)]
        assert set(changed).issubset({selected})
        for gene, (lo, hi) in M.BOUNDS.items():
            assert lo <= getattr(child, gene) <= hi


def test_weight_is_long_cash_and_uses_only_past():
    returns = M.simulate_market(11, "development")
    genome = M.Genome(60, 30, 0.10, 0.60, 0.10)
    t = 300
    original = M.weight(genome, returns, t)
    altered = returns.copy()
    altered[t:] = 999
    assert np.allclose(original, M.weight(genome, altered, t))
    assert (original >= 0).all()
    assert original.sum() <= 1 + 1e-12


def test_market_is_deterministic_and_families_differ():
    a = M.simulate_market(3, "development")
    b = M.simulate_market(3, "development")
    c = M.simulate_market(3, "confirmation")
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_equal_candidate_budget_small_run():
    returns = M.simulate_market(5, "development")
    rng = np.random.default_rng(99)
    initial = [M.draw_genome(rng) for _ in range(M.POPULATION)]
    _, _, _, random_n = M.method_path("random", returns, initial, 1)
    _, _, _, evolution_n = M.method_path("evolution", returns, initial, 2)
    assert random_n == evolution_n
