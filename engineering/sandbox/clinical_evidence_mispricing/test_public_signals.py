import pandas as pd
import pytest

from .public_signals import (
    PublicSignal,
    clinicaltrials_collaborator_signals,
    lead_time_days,
    qualifies_costly_external_commitment,
    signals_available_by,
    usaspending_award_search_request,
    usaspending_award_signals,
    validate_unique_signal_ids,
)


def _signal(**overrides) -> PublicSignal:
    values = {
        "signal_id": "SIG-001",
        "signal_type": "manufacturing_commitment",
        "focal_entity": "Sponsor",
        "related_entity": "Supplier",
        "asset_id": "NCT00000001",
        "published_at": "2024-01-01 12:00Z",
        "source_url": "https://example.test/signal",
        "action_date": "2023-12-28",
        "amount_usd": 10_000_000,
    }
    values.update(overrides)
    return PublicSignal(**values)


def test_selection_uses_publication_time_not_action_date() -> None:
    signal = _signal(
        action_date="2023-01-01",
        published_at="2024-02-01 12:00Z",
    )
    assert signals_available_by(
        [signal],
        decision_at="2024-01-15 12:00Z",
        asset_id="NCT00000001",
    ) == []


def test_general_company_signal_requires_explicit_inclusion() -> None:
    signal = _signal(asset_id=None)
    assert signals_available_by(
        [signal],
        decision_at="2024-01-15 12:00Z",
        asset_id="NCT00000001",
    ) == []
    assert signals_available_by(
        [signal],
        decision_at="2024-01-15 12:00Z",
        asset_id="NCT00000001",
        include_general=True,
    ) == [signal]


def test_duplicate_signal_ids_are_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        validate_unique_signal_ids([_signal(), _signal()])


def test_lead_time_uses_publication_timestamp() -> None:
    assert lead_time_days(
        _signal(published_at="2024-01-01 12:00Z"),
        event_at="2024-01-11 12:00Z",
    ) == 10.0


def test_extracts_asset_specific_clinicaltrials_collaborators() -> None:
    study = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCT00000001"},
            "sponsorCollaboratorsModule": {
                "leadSponsor": {"name": "Sponsor"},
                "collaborators": [
                    {"name": "BARDA", "class": "FED"},
                    {"name": "Supplier", "class": "INDUSTRY"},
                ],
            },
        }
    }
    signals = clinicaltrials_collaborator_signals(
        study,
        observed_public_at="2024-01-01 12:00Z",
        source_url="https://clinicaltrials.gov/study/NCT00000001",
    )
    assert {signal.related_entity for signal in signals} == {"BARDA", "Supplier"}
    assert all(signal.asset_id == "NCT00000001" for signal in signals)


def test_usaspending_request_is_bounded_and_deterministic() -> None:
    request = usaspending_award_search_request(
        recipient_name="MODERNATX, INC.",
        start_date="2019-01-01",
        end_date="2021-12-31",
        limit=25,
    )
    assert request["filters"]["recipient_search_text"] == ["MODERNATX, INC."]
    assert request["limit"] == 25
    assert request["sort"] == "Base Obligation Date"


def test_current_usaspending_response_is_not_backdated() -> None:
    response = {
        "results": [
            {
                "Award ID": "75A50120C00034",
                "Recipient Name": "MODERNATX, INC.",
                "Awarding Agency": "Department of Health and Human Services",
                "Awarding Sub Agency": "Office of the Assistant Secretary for Health",
                "Base Obligation Date": "2020-04-16",
                "Award Amount": 483_000_000,
            }
        ]
    }
    signal = usaspending_award_signals(
        response,
        retrieved_at="2026-08-21 12:00Z",
        source_url="https://api.usaspending.gov/api/v2/search/spending_by_award/",
    )[0]
    assert signal.action_date == pd.Timestamp("2020-04-16").date()
    assert signal.published_at == pd.Timestamp("2026-08-21 12:00Z")
    assert signal.availability_precision == "retrieval_only"
    assert signals_available_by(
        [signal],
        decision_at="2020-11-16 12:00Z",
        include_general=True,
    ) == []


def test_current_clinicaltrials_observation_is_retrieval_only() -> None:
    study = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCT00000001"},
            "sponsorCollaboratorsModule": {
                "leadSponsor": {"name": "Sponsor"},
                "collaborators": [{"name": "BARDA"}],
            },
        }
    }
    signal = clinicaltrials_collaborator_signals(
        study,
        observed_public_at="2026-08-21 12:00Z",
        source_url="https://clinicaltrials.gov/study/NCT00000001",
    )[0]
    assert signal.availability_precision == "retrieval_only"


def test_unknown_availability_precision_is_rejected() -> None:
    with pytest.raises(ValueError, match="availability_precision"):
        _signal(availability_precision="guessed")


@pytest.mark.parametrize("precision", ["exact", "date_upper_bound"])
def test_costly_asset_specific_external_commitment_qualifies(precision: str) -> None:
    signal = _signal(
        availability_precision=precision,
        costly_or_irreversible=True,
    )
    assert qualifies_costly_external_commitment(
        signal,
        event_at="2024-04-01 12:00Z",
    )


@pytest.mark.parametrize(
    "overrides",
    [
        {"availability_precision": "retrieval_only"},
        {"asset_id": None},
        {"external_party": False},
        {"costly_or_irreversible": False},
    ],
)
def test_weak_or_historically_unavailable_activity_does_not_qualify(
    overrides: dict,
) -> None:
    values = {"costly_or_irreversible": True, **overrides}
    signal = _signal(**values)
    assert not qualifies_costly_external_commitment(
        signal,
        event_at="2024-04-01 12:00Z",
    )


@pytest.mark.parametrize(
    "event_at",
    ["2024-01-15 12:00Z", "2025-02-01 12:00Z"],
)
def test_commitments_outside_frozen_lead_window_do_not_qualify(event_at: str) -> None:
    signal = _signal(costly_or_irreversible=True)
    assert not qualifies_costly_external_commitment(signal, event_at=event_at)
