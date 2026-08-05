import importlib.util
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("exp031", Path(__file__).with_name("analysis.py"))
analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(analysis)


def test_factorial_cells_and_trigger_boundaries() -> None:
    assert len(analysis.POLICIES) == 4
    assert analysis.should_trigger("early", 2.91, 1.2)
    assert not analysis.should_trigger("breach", 2.91, 1.2)
    assert analysis.should_trigger("breach", 3.01, 1.2)
    assert analysis.should_trigger("early", 2.0, 1.04)


def test_frozen_base_path_and_state() -> None:
    assert analysis.BASE_PATH.exists()
    assert analysis.base.FAMILIES == (
        "liquidity_drain", "leverage_cancer", "systemic_correlation", "combined", "benign_volatility")
    assert analysis.base.DAYS == 120


def test_same_path_for_all_factorial_cells() -> None:
    first = analysis.base.return_path("liquidity_drain", 30000)
    second = analysis.base.return_path("liquidity_drain", 30000)
    assert (first == second).all()

