import numpy as np
import pandas as pd

from engineering.argus_lab.statistics import clustered_mean, hc3_ols


def test_hc3_ols_recovers_linear_relation():
    x = pd.DataFrame({"x": np.arange(20, dtype=float)})
    y = 1.0 + 2.0 * x["x"]
    result = hc3_ols(y, x)
    assert np.isclose(result.params["const"], 1.0)
    assert np.isclose(result.params["x"], 2.0)


def test_clustered_mean_returns_expected_mean():
    values = pd.Series([1.0, 1.0, 3.0, 3.0])
    groups = pd.Series(["a", "a", "b", "b"])
    mean, se, t_stat = clustered_mean(values, groups)
    assert np.isclose(mean, 2.0)
    assert se > 0
    assert np.isclose(t_stat, mean / se)
