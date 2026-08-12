import importlib.util
from pathlib import Path

import pandas as pd


PATH = Path(__file__).with_name("eba_2025_schema_audit.py")
SPEC = importlib.util.spec_from_file_location("eba_schema_audit", PATH)
audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(audit)


def test_counts_stringifies_keys_and_preserves_missing() -> None:
    result = audit.counts(pd.Series([2, 2, 3, None]))
    assert result["2.0"] == 2
    assert result["3.0"] == 1
    assert result["nan"] == 1


def test_profile_csv_reports_coverage(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    pd.DataFrame(
        {
            "LEI_Code": ["A", "A", "B"],
            "Period": [202412, 202512, 202512],
            "Scenario": [11, 2, 2],
            "Item": [1, 1, 2],
            "Amount": [1.0, None, 3.0],
        }
    ).to_csv(path, index=False)
    result = audit.profile_csv(path)
    assert result["rows"] == 3
    assert result["banks"] == 2
    assert result["missing_amounts"] == 1
    assert result["exact_duplicate_rows"] == 0
