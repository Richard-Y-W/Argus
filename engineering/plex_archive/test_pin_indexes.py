import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("pin_indexes", HERE / "pin_indexes.py")
M = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def entry(time, size):
    return {"name": time, "url": time, "size": size, "last_modified": time,
            "etag": time, "file_time": f"2025-07-08T{time}Z"}


def test_choose_nearest_valid_target():
    files = [entry("11:45:00", 20_000_000), entry("12:15:05", 19_000_000),
             entry("12:45:00", 20_000_000)]
    selected, audit = M.choose_file(files)
    assert selected["name"] == "12:15:05"
    assert audit["invalid_below_half_median"] == 0


def test_rejects_tiny_incomplete_file():
    files = [entry("12:15:00", 1_000_000), entry("11:45:00", 20_000_000),
             entry("12:45:00", 20_000_000)]
    selected, audit = M.choose_file(files)
    assert selected["name"] == "11:45:00"
    assert audit["invalid_below_half_median"] == 1


def test_rejects_large_time_substitution():
    selected, audit = M.choose_file([entry("16:45:00", 20_000_000)])
    assert selected is None
    assert audit["selected_offset_seconds"] > 1860
