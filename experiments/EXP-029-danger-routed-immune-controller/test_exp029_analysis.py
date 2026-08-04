import importlib.util
from pathlib import Path

import numpy as np


SPEC = importlib.util.spec_from_file_location("exp029", Path(__file__).with_name("analysis.py"))
analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(analysis)


def test_routes_are_exhaustive() -> None:
    thresholds = {"danger_q75": 2.0, "localization_q70": 0.4}
    assert analysis.controller_route(1.9, 0.9, thresholds) == "tolerate"
    assert analysis.controller_route(2.0, 0.4, thresholds) == "localized"
    assert analysis.controller_route(2.1, 0.39, thresholds) == "systemic"


def test_local_response_preserves_other_modules() -> None:
    rng = np.random.default_rng(3)
    train = rng.normal(0, 0.01, (252, 10))
    train[-63:, 8] += 0.03
    incumbent = np.full(10, 0.1)
    pool = analysis.candidates("localized", train, incumbent, 12)
    changed = set(np.argsort(analysis.damage_scores(train))[-2:])
    unchanged = list(set(range(10)) - changed)
    assert pool.shape == (64, 10)
    assert np.allclose(pool.sum(1), 1)
    assert np.allclose(pool[:, unchanged], 0.1)


def test_equal_fixed_budgets_and_loader() -> None:
    frame = analysis.load_french_zip(analysis.RAW / "archive_202412.zip")
    assert frame.shape[1] == 10
    assert frame.index.max().year == 2024
    incumbent = np.full(10, 0.1)
    train = frame.iloc[-252:].to_numpy()
    for response in ("localized", "all_gene", "random"):
        assert analysis.candidates(response, train, incumbent, 5).shape == (64, 10)

