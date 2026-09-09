from __future__ import annotations

import pytest

from .probe_positive_spike_reversal import parse_adjusted_close


def test_parse_adjusted_close_drops_missing_values() -> None:
    payload = {
        "chart": {
            "error": None,
            "result": [
                {
                    "timestamp": [1_704_067_200, 1_704_153_600, 1_704_240_000],
                    "indicators": {
                        "adjclose": [{"adjclose": [10.0, None, 11.0]}]
                    },
                }
            ],
        }
    }

    result = parse_adjusted_close(payload)

    assert result.tolist() == [10.0, 11.0]
    assert str(result.index.tz) == "UTC"


def test_parse_adjusted_close_rejects_provider_error() -> None:
    payload = {"chart": {"error": {"code": "Not Found"}, "result": None}}

    with pytest.raises(ValueError, match="provider error"):
        parse_adjusted_close(payload)


def test_parse_adjusted_close_rejects_length_mismatch() -> None:
    payload = {
        "chart": {
            "error": None,
            "result": [
                {
                    "timestamp": [1, 2],
                    "indicators": {"adjclose": [{"adjclose": [10.0]}]},
                }
            ],
        }
    }

    with pytest.raises(ValueError, match="lengths differ"):
        parse_adjusted_close(payload)
