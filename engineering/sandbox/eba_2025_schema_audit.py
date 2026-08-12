"""Profile the official EBA 2025 stress-test release without estimating effects.

Usage:
    python engineering/sandbox/eba_2025_schema_audit.py DATA_DIR [OUTPUT_JSON]

DATA_DIR must contain the five files listed in datasets/eba_2025_stress_test.md.
The script is a feasibility probe. Its output cannot support a research claim.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd


FILES = (
    "TRA_OTH.csv",
    "TRA_CRE_IRB.csv",
    "TRA_CRE_STA.csv",
    "Data_Dictionary.xlsx",
    "Metadata_TR.xlsx",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def counts(series: pd.Series) -> dict[str, int]:
    return {str(key): int(value) for key, value in series.value_counts(dropna=False).sort_index().items()}


def profile_csv(path: Path) -> dict[str, object]:
    frame = pd.read_csv(path)
    return {
        "rows": int(len(frame)),
        "columns": frame.columns.tolist(),
        "banks": int(frame["LEI_Code"].nunique()),
        "periods": counts(frame["Period"]),
        "scenarios": counts(frame["Scenario"]),
        "items": counts(frame["Item"]),
        "missing_amounts": int(frame["Amount"].isna().sum()),
        "exact_duplicate_rows": int(frame.duplicated().sum()),
    }


def audit(data_dir: Path) -> dict[str, object]:
    missing = [name for name in FILES if not (data_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing required files: {', '.join(missing)}")

    dictionary = pd.read_excel(data_dir / "Data_Dictionary.xlsx", sheet_name="SDD")
    metadata = pd.ExcelFile(data_dir / "Metadata_TR.xlsx")
    liquidity = dictionary[
        dictionary["Label"].str.contains("liquid|liquidity|funding|deposit", case=False, na=False)
    ][["Template", "Item", "Label"]]

    return {
        "files": {
            name: {"bytes": (data_dir / name).stat().st_size, "sha256": sha256(data_dir / name)}
            for name in FILES
        },
        "tables": {name: profile_csv(data_dir / name) for name in FILES[:3]},
        "dictionary": {
            "rows": int(len(dictionary)),
            "templates": counts(dictionary["Template"]),
            "liquidity_or_funding_labels": liquidity.to_dict(orient="records"),
        },
        "metadata_sheets": metadata.sheet_names,
        "bank_metadata_rows": int(pd.read_excel(data_dir / "Metadata_TR.xlsx", sheet_name="ListOfBanks").shape[0]),
    }


def main() -> None:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: eba_2025_schema_audit.py DATA_DIR [OUTPUT_JSON]")
    report = audit(Path(sys.argv[1]))
    rendered = json.dumps(report, indent=2) + "\n"
    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
