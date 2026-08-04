import bz2
import csv
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("plex_extract", HERE / "extract_plex.py")
M = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def write_fixture(path: Path, rows: list[dict], fields=None):
    fields = fields or sorted(M.REQUIRED)
    with bz2.open(path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def base_row(**changes):
    row = {field: "1" for field in M.REQUIRED}
    row.update({"type_id": "44992", "region_id": "10000002", "is_buy_order": "true",
                "volume_remain": "25", "price": "4000000"})
    row.update(changes)
    return row


def test_stream_filters_plex_and_counts_regions(tmp_path):
    path = tmp_path / "fixture.csv.bz2"
    rows = [base_row(), base_row(region_id="10000043", is_buy_order="false", volume_remain="10"),
            base_row(type_id="34", volume_remain="999")]
    write_fixture(path, rows)
    summary, filtered = M.stream_snapshot(path, keep_rows=True)
    assert summary["total_rows"] == 3
    assert summary["plex_orders"] == 2
    assert summary["distinct_plex_regions"] == 2
    assert summary["plex_buy_volume"] == 25 and summary["plex_sell_volume"] == 10
    assert not summary["global_region_only"]
    assert len(filtered) == 2


def test_global_region_classification(tmp_path):
    path = tmp_path / "fixture.csv.bz2"
    write_fixture(path, [base_row(region_id=M.GLOBAL_REGION_ID)])
    summary, _ = M.stream_snapshot(path)
    assert summary["global_region_only"]


def test_missing_schema_fails(tmp_path):
    path = tmp_path / "fixture.csv.bz2"
    fields = sorted(M.REQUIRED - {"region_id"})
    write_fixture(path, [{key: value for key, value in base_row().items() if key in fields}], fields)
    try:
        M.stream_snapshot(path)
    except ValueError as error:
        assert "region_id" in str(error)
    else:
        raise AssertionError("missing required field was accepted")

