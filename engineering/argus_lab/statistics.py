"""Auditable statistical helpers; deliberately thin wrappers."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def hc3_ols(y: pd.Series, x: pd.DataFrame, add_constant: bool = True):
    """Fit OLS with HC3 standard errors and return the fitted result."""
    design = sm.add_constant(x, has_constant="add") if add_constant else x
    return sm.OLS(y, design, missing="drop").fit(cov_type="HC3")


def clustered_mean(values: pd.Series, groups: pd.Series) -> tuple[float, float, float]:
    """Mean, cluster-robust standard error, and t-statistic against zero."""
    frame = pd.DataFrame({"value": values, "group": groups}).dropna()
    result = sm.OLS(frame["value"], np.ones((len(frame), 1))).fit(
        cov_type="cluster", cov_kwds={"groups": frame["group"]}
    )
    mean = float(result.params.iloc[0] if hasattr(result.params, "iloc") else result.params[0])
    se = float(result.bse.iloc[0] if hasattr(result.bse, "iloc") else result.bse[0])
    return mean, se, mean / se
