from pathlib import Path

import pandas as pd

from .audit import audit_rtdsm, audit_spf


def test_spf_audit_separates_point_and_density_horizons(tmp_path: Path):
    point = pd.DataFrame(
        {
            "YEAR": [2025, 2025], "QUARTER": [1, 1], "ID": [1, 2], "INDUSTRY": [1, 2],
            **{f"COREPCE{i}": [2.0, 2.1] for i in range(2, 7)},
        }
    )
    density = pd.DataFrame(
        {
            "YEAR": [2025], "QUARTER": [1], "ID": [1], "INDUSTRY": [1],
            **{f"PRCPCE{i}": [10.0] for i in range(1, 21)},
        }
    )
    workbook = tmp_path / "spf.xlsx"
    with pd.ExcelWriter(workbook) as writer:
        point.to_excel(writer, sheet_name="COREPCE", index=False)
        density.to_excel(writer, sheet_name="PRCPCE", index=False)

    result = audit_spf(workbook)
    assert result["three_point_horizon_gate"] is True
    assert result["three_density_horizon_gate"] is False
    assert result["density_rows_with_bad_probability_sum"] == 0


def test_rtdsm_audit_ignores_empty_declared_vintages(tmp_path: Path):
    files = {}
    for prefix in ("ROUTPUT", "CPI", "RUC"):
        frame = pd.DataFrame(
            {"DATE": ["2024:Q1", "2024:Q2"], f"{prefix}23Q4": [None, None], f"{prefix}24Q3": [1.0, 2.0]}
        )
        path = tmp_path / f"{prefix}.xlsx"
        frame.to_excel(path, index=False)
        files[prefix] = path

    result = audit_rtdsm(files)
    assert result["common_quarterly_vintage_count"] == 1
    assert result["common_first_as_of"] == "2024-08-15"
    assert result["three_target_quarterly_gate"] is True
    assert result["series"]["CPI"]["empty_leading_vintage_columns"] == 1
