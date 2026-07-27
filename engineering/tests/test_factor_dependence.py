import numpy as np
import pandas as pd
import pytest

from engineering.argus_lab.factor_dependence import effective_rank, exact_sign_pvalue


def test_effective_rank_matches_identity_and_duplicate_extremes():
    identity = pd.DataFrame(np.eye(4))
    duplicate = pd.DataFrame(np.ones((4, 4)))
    assert effective_rank(identity) == 4.0
    assert effective_rank(duplicate) == pytest.approx(1.0)


def test_exact_sign_test_enumerates_all_assignments():
    assert exact_sign_pvalue(pd.Series([1.0, 1.0, 1.0])) == 0.25
    assert exact_sign_pvalue(pd.Series([1.0, -1.0])) == 1.0
