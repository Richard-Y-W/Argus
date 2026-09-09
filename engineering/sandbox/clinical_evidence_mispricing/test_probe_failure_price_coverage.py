from __future__ import annotations

import pandas as pd

from .probe_failure_price_coverage import has_event_window


def test_has_event_window_requires_full_estimation_and_post_period() -> None:
    enough = pd.Series(1.0, index=pd.bdate_range("2017-01-02", periods=500))
    too_short = pd.Series(1.0, index=pd.bdate_range("2018-01-02", periods=120))

    assert has_event_window(enough, "2018-03-01")
    assert not has_event_window(too_short, "2018-03-01")
