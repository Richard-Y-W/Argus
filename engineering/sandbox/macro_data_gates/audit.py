"""Deterministic, return-free audits of SPF and RTDSM workbooks.

These checks establish data feasibility only. They do not estimate a forecasting,
economic, or asset-pricing result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


POINT_HORIZONS = [f"COREPCE{i}" for i in range(2, 7)]
DENSITY_HORIZONS = [
    [f"PRCPCE{i}" for i in range(1, 11)],
    [f"PRCPCE{i}" for i in range(11, 21)],
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _survey_sets(frame: pd.DataFrame, columns: list[str]) -> list[set[int]]:
    sets: list[set[int]] = []
    for _, group in frame.groupby(["YEAR", "QUARTER"], sort=True):
        mask = group[columns].notna().any(axis=1)
        sets.append(set(group.loc[mask, "ID"].astype(int)))
    return sets


def _nanmedian_or_nan(values: list[float]) -> float:
    finite = [value for value in values if not np.isnan(value)]
    return float(np.median(finite)) if finite else float("nan")


def audit_spf(workbook: Path) -> dict[str, object]:
    point = pd.read_excel(workbook, sheet_name="COREPCE")
    density = pd.read_excel(workbook, sheet_name="PRCPCE")

    point = point.loc[point[POINT_HORIZONS].notna().any(axis=1)].copy()
    surveys = point[["YEAR", "QUARTER"]].drop_duplicates()
    point_complete = point[POINT_HORIZONS].notna().all(axis=1)

    within_survey_shares: list[float] = []
    for _, group in point.groupby(["YEAR", "QUARTER"], sort=True):
        responders = [set(group.loc[group[col].notna(), "ID"].astype(int)) for col in POINT_HORIZONS]
        union = set().union(*responders)
        intersection = set.intersection(*responders)
        within_survey_shares.append(len(intersection) / len(union) if union else np.nan)

    participant_sets = _survey_sets(point, POINT_HORIZONS)
    retention = [
        len(previous & current) / len(previous) if previous else np.nan
        for previous, current in zip(participant_sets, participant_sets[1:])
    ]

    density = density.loc[density[DENSITY_HORIZONS[0] + DENSITY_HORIZONS[1]].notna().any(axis=1)].copy()
    density_sums = [density[columns].sum(axis=1, min_count=len(columns)) for columns in DENSITY_HORIZONS]
    complete_density = pd.concat([series.notna() for series in density_sums], axis=1).all(axis=1)
    bad_sums = pd.concat(
        [(series.notna() & ~np.isclose(series, 100.0, atol=0.11)) for series in density_sums],
        axis=1,
    ).any(axis=1)

    participation = point.groupby("ID").size()
    return {
        "workbook_sha256": sha256(workbook),
        "survey_first": f"{int(surveys.iloc[0].YEAR)}:Q{int(surveys.iloc[0].QUARTER)}",
        "survey_last": f"{int(surveys.iloc[-1].YEAR)}:Q{int(surveys.iloc[-1].QUARTER)}",
        "survey_count": int(len(surveys)),
        "unique_ids": int(point["ID"].nunique()),
        "point_horizon_count": len(POINT_HORIZONS),
        "point_response_counts": {column: int(point[column].notna().sum()) for column in POINT_HORIZONS},
        "complete_point_response_share": float(point_complete.mean()),
        "median_within_survey_common_horizon_share": _nanmedian_or_nan(within_survey_shares),
        "median_adjacent_survey_retention": _nanmedian_or_nan(retention),
        "median_surveys_per_id": float(participation.median()),
        "max_surveys_per_id": int(participation.max()),
        "density_horizon_count": len(DENSITY_HORIZONS),
        "complete_density_rows": int(complete_density.sum()),
        "density_rows_with_bad_probability_sum": int(bad_sums.sum()),
        "three_point_horizon_gate": all(point[column].notna().sum() > 0 for column in POINT_HORIZONS[:3]),
        "three_density_horizon_gate": len(DENSITY_HORIZONS) >= 3,
    }


def _usable_vintages(frame: pd.DataFrame) -> list[str]:
    return [str(column) for column in frame.columns[1:] if frame[column].notna().any()]


def _quarter_suffix(column: str) -> str:
    match = re.search(r"(\d{2}Q[1-4])$", column)
    if not match:
        raise ValueError(f"not a quarterly vintage column: {column}")
    return match.group(1)


def _as_of_date(suffix: str) -> str:
    year_two = int(suffix[:2])
    year = 1900 + year_two if year_two >= 40 else 2000 + year_two
    quarter = int(suffix[-1])
    month = {1: 2, 2: 5, 3: 8, 4: 11}[quarter]
    return f"{year:04d}-{month:02d}-15"


def audit_rtdsm(workbooks: dict[str, Path]) -> dict[str, object]:
    details: dict[str, object] = {}
    suffix_sets: list[set[str]] = []
    for name, path in workbooks.items():
        frame = pd.read_excel(path)
        usable = _usable_vintages(frame)
        suffixes = {_quarter_suffix(column) for column in usable}
        suffix_sets.append(suffixes)
        latest = usable[-1]
        latest_rows = frame.loc[frame[latest].notna(), frame.columns[0]]
        details[name] = {
            "sha256": sha256(path),
            "observation_rows": int(len(frame)),
            "declared_vintage_columns": int(len(frame.columns) - 1),
            "usable_vintage_columns": int(len(usable)),
            "empty_leading_vintage_columns": int(len(frame.columns) - 1 - len(usable)),
            "first_usable_vintage": usable[0],
            "last_usable_vintage": latest,
            "latest_observation": str(latest_rows.iloc[-1]),
            "duplicate_observation_dates": int(frame.iloc[:, 0].duplicated().sum()),
        }

    common = set.intersection(*suffix_sets)
    ordered_common = sorted(common, key=_as_of_date)
    return {
        "series": details,
        "common_quarterly_vintage_count": len(common),
        "common_first_as_of": _as_of_date(ordered_common[0]),
        "common_last_as_of": _as_of_date(ordered_common[-1]),
        "three_target_quarterly_gate": len(workbooks) >= 3 and len(common) > 0,
        "exact_release_mapping_available": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="audit", required=True)
    spf = subparsers.add_parser("spf")
    spf.add_argument("workbook", type=Path)
    rtdsm = subparsers.add_parser("rtdsm")
    rtdsm.add_argument("--routput", required=True, type=Path)
    rtdsm.add_argument("--cpi", required=True, type=Path)
    rtdsm.add_argument("--ruc", required=True, type=Path)
    args = parser.parse_args()
    if args.audit == "spf":
        result = audit_spf(args.workbook)
    else:
        result = audit_rtdsm({"ROUTPUT": args.routput, "CPI": args.cpi, "RUC": args.ruc})
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
