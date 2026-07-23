from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from engineering.argus_lab.jkp_decay import (
    assign_jkp_windows,
    eligible_factor_locations,
    fit_row,
    load_eligible_us,
    parse_jkp_metadata,
    window_fit,
)


ROOT = Path(__file__).resolve().parents[2]


def test_metadata_parser_records_exclusion_reasons():
    raw = pd.DataFrame(
        {
            "abr_jkp": ["valid", "early", "duplicate", "duplicate", "missing-years", None],
            "in-sample period": ["1990-2000", "1990-2005", "1991-2001", "1991-2001", "unknown", "1990-2000"],
            "cite": ["Paper (2002)", "Paper (2004)", "Paper (2003)", "Paper (2003)", "Paper", "Paper (2002)"],
            "significance": [1, 1, 0, 0, 1, 1],
        }
    )
    eligible, flow = parse_jkp_metadata(raw)
    assert eligible.name.tolist() == ["valid"]
    assert flow.reason.tolist() == [
        "eligible",
        "publication_before_sample_end",
        "duplicate_name",
        "duplicate_name",
        "missing_or_ambiguous_year",
        "missing_name",
    ]


def test_windows_include_boundary_years_and_enforce_twelve_month_floor():
    dates = pd.date_range("2000-01-31", "2002-12-31", freq="ME")
    panel = pd.DataFrame(
        {
            "name": "factor",
            "date": dates,
            "ret": 0.0,
            "sample_start": 2000,
            "sample_end": 2000,
            "publication_year": 2001,
        }
    )
    windowed = assign_jkp_windows(panel)
    assert windowed.groupby("window").size().to_dict() == {
        "in_sample": 12,
        "post_sample": 12,
        "post_pub": 12,
    }
    assert eligible_factor_locations(windowed).name.tolist() == ["factor"]
    assert eligible_factor_locations(windowed.iloc[:-1]).empty


def test_window_estimator_has_frozen_balanced_fixture_estimands():
    dates = pd.date_range("2000-01-31", periods=6, freq="ME")
    windows = ["in_sample", "in_sample", "post_sample", "post_sample", "post_pub", "post_pub"]
    panel = pd.concat(
        [
            pd.DataFrame({"name": "a", "date": dates, "window": windows, "ret": [1, 1, 2, 2, 4, 4]}),
            pd.DataFrame({"name": "b", "date": dates, "window": windows, "ret": [2, 2, 4, 4, 8, 8]}),
        ],
        ignore_index=True,
    )
    row = fit_row(window_fit(panel), "fixture", len(panel), panel.name.nunique())
    assert np.isclose(row["post_sample_pct"], 150.0)
    assert np.isclose(row["post_pub_pct"], 450.0)
    assert np.isclose(row["postpub_minus_postsample_pct"], 300.0)


def test_local_jkp_estimate_matches_committed_exp016_golden():
    required = [
        ROOT / "datasets/raw/jkp_factor_details.xlsx",
        ROOT / "datasets/raw/jkp_usa/[usa]_[all_factors]_[monthly]_[vw].csv",
    ]
    if not all(path.exists() for path in required):
        pytest.skip("licensed JKP files are not available in data-free CI")
    expected = pd.read_csv(ROOT / "experiments/EXP-016-standalone-us-jkp-decay/results/estimates.csv")
    expected = expected.set_index("spec").loc["usa"]
    panel = load_eligible_us(ROOT)
    actual = pd.Series(fit_row(window_fit(panel), "usa", len(panel), panel.name.nunique()))
    numeric = [
        "observations",
        "factors",
        "post_sample_pct",
        "post_sample_t",
        "post_pub_pct",
        "post_pub_t",
        "postpub_minus_postsample_pct",
        "contrast_t",
    ]
    np.testing.assert_allclose(
        actual[numeric].astype(float), expected[numeric].astype(float), rtol=0, atol=1e-10
    )
