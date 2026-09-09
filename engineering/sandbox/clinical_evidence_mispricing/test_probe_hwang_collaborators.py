from pathlib import Path

from .probe_hwang_collaborators import (
    DEFAULT_EVENTS,
    extract_current_collaborators,
    load_events,
)


def test_hwang_seed_matches_published_sample_counts() -> None:
    events = load_events(DEFAULT_EVENTS)
    assert len(events) == 24
    assert sum(event["outcome"] == "positive" for event in events) == 16
    assert sum(event["outcome"] == "negative" for event in events) == 8
    assert sum(event["phase"] == "3" for event in events) == 13
    assert len({event["nct_id"] for event in events}) == 23


def test_extract_current_collaborators_ignores_blank_names() -> None:
    study = {
        "protocolSection": {
            "sponsorCollaboratorsModule": {
                "collaborators": [
                    {"name": "BARDA"},
                    {"name": ""},
                    {},
                ]
            }
        }
    }
    assert extract_current_collaborators(study) == ["BARDA"]


def test_default_event_fixture_exists() -> None:
    assert isinstance(DEFAULT_EVENTS, Path)
    assert DEFAULT_EVENTS.exists()
