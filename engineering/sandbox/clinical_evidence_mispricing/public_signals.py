"""Public collaborator and capacity-signal contracts for exploratory work."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Iterable, Mapping

import pandas as pd


ALLOWED_SIGNAL_TYPES = {
    "trial_collaboration",
    "government_award",
    "manufacturing_commitment",
    "supply_procurement",
    "insurance_disclosure",
}

ALLOWED_AVAILABILITY_PRECISIONS = {
    "exact",
    "date_upper_bound",
    "retrieval_only",
}


def _utc(value: Any, *, field: str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        raise ValueError(f"{field} must be timezone-aware")
    return timestamp.tz_convert("UTC")


@dataclass(frozen=True)
class PublicSignal:
    signal_id: str
    signal_type: str
    focal_entity: str
    related_entity: str
    published_at: pd.Timestamp
    source_url: str
    asset_id: str | None = None
    action_date: date | None = None
    amount_usd: float | None = None
    availability_precision: str = "exact"
    external_party: bool = True
    costly_or_irreversible: bool = False
    government_risk_share: bool = False

    def __post_init__(self) -> None:
        required = {
            "signal_id": self.signal_id,
            "focal_entity": self.focal_entity,
            "related_entity": self.related_entity,
            "source_url": self.source_url,
        }
        for field, value in required.items():
            if not value.strip():
                raise ValueError(f"{field} must be non-empty")
        if self.signal_type not in ALLOWED_SIGNAL_TYPES:
            raise ValueError(f"unsupported signal_type: {self.signal_type}")
        if self.availability_precision not in ALLOWED_AVAILABILITY_PRECISIONS:
            raise ValueError(
                f"unsupported availability_precision: {self.availability_precision}"
            )
        object.__setattr__(
            self,
            "published_at",
            _utc(self.published_at, field="published_at"),
        )
        if self.action_date is not None:
            object.__setattr__(self, "action_date", pd.Timestamp(self.action_date).date())

    @property
    def is_asset_specific(self) -> bool:
        return self.asset_id is not None

    @property
    def is_historically_eligible(self) -> bool:
        return self.availability_precision != "retrieval_only"


def validate_unique_signal_ids(signals: Iterable[PublicSignal]) -> list[PublicSignal]:
    materialized = list(signals)
    identifiers = [signal.signal_id for signal in materialized]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("duplicate public signal identifiers")
    return materialized


def signals_available_by(
    signals: Iterable[PublicSignal],
    *,
    decision_at: Any,
    asset_id: str | None = None,
    include_general: bool = False,
) -> list[PublicSignal]:
    """Select signals by public timestamp, never by underlying action date."""
    cutoff = _utc(decision_at, field="decision_at")
    selected: list[PublicSignal] = []
    for signal in validate_unique_signal_ids(signals):
        if signal.published_at > cutoff:
            continue
        if asset_id is None:
            selected.append(signal)
        elif signal.asset_id == asset_id:
            selected.append(signal)
        elif include_general and signal.asset_id is None:
            selected.append(signal)
    return sorted(selected, key=lambda signal: (signal.published_at, signal.signal_id))


def lead_time_days(signal: PublicSignal, *, event_at: Any) -> float:
    event_timestamp = _utc(event_at, field="event_at")
    return float((event_timestamp - signal.published_at).total_seconds() / 86_400)


def qualifies_costly_external_commitment(
    signal: PublicSignal,
    *,
    event_at: Any,
    minimum_lead_days: float = 30,
    maximum_lead_days: float = 365,
) -> bool:
    """Apply the frozen exploratory commitment rule without using outcomes.

    ``date_upper_bound`` timestamps must already encode a conservative latest
    public time for the date. Retrieval-only observations are discovery aids and
    cannot qualify as historical signals.
    """
    if minimum_lead_days < 0 or maximum_lead_days < minimum_lead_days:
        raise ValueError("lead-day bounds are invalid")
    days = lead_time_days(signal, event_at=event_at)
    return (
        signal.is_historically_eligible
        and signal.is_asset_specific
        and signal.external_party
        and signal.costly_or_irreversible
        and minimum_lead_days <= days <= maximum_lead_days
    )


def clinicaltrials_collaborator_signals(
    study: Mapping[str, Any],
    *,
    observed_public_at: Any,
    source_url: str,
    availability_precision: str = "retrieval_only",
) -> list[PublicSignal]:
    """Extract sponsor-collaborator edges from one observed CT.gov version."""
    protocol = study.get("protocolSection", {})
    identity = protocol.get("identificationModule", {})
    sponsors = protocol.get("sponsorCollaboratorsModule", {})
    nct_id = identity.get("nctId")
    lead_sponsor = sponsors.get("leadSponsor", {}).get("name")
    if not nct_id or not lead_sponsor:
        raise ValueError("ClinicalTrials.gov record lacks NCT ID or lead sponsor")

    signals = []
    for collaborator in sponsors.get("collaborators", []):
        collaborator_name = collaborator.get("name")
        if not collaborator_name:
            raise ValueError("ClinicalTrials.gov collaborator lacks a name")
        signals.append(
            PublicSignal(
                signal_id=f"ctgov:{nct_id}:{collaborator_name}",
                signal_type="trial_collaboration",
                focal_entity=lead_sponsor,
                related_entity=collaborator_name,
                asset_id=nct_id,
                published_at=observed_public_at,
                source_url=source_url,
                availability_precision=availability_precision,
            )
        )
    return validate_unique_signal_ids(signals)


def usaspending_award_search_request(
    *,
    recipient_name: str,
    start_date: str,
    end_date: str,
    limit: int = 100,
) -> dict[str, Any]:
    """Build a deterministic USAspending award-level search request."""
    if not recipient_name.strip():
        raise ValueError("recipient_name must be non-empty")
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    if pd.Timestamp(start_date) > pd.Timestamp(end_date):
        raise ValueError("start_date must not follow end_date")
    return {
        "filters": {
            "recipient_search_text": [recipient_name],
            "time_period": [{"start_date": start_date, "end_date": end_date}],
            "award_type_codes": ["A", "B", "C", "D", "02", "03", "04", "05"],
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Award Amount",
            "Awarding Agency",
            "Awarding Sub Agency",
            "Description",
            "Last Modified Date",
            "Base Obligation Date",
        ],
        "page": 1,
        "limit": limit,
        "sort": "Base Obligation Date",
        "order": "asc",
        "spending_level": "awards",
    }


def usaspending_award_signals(
    response: Mapping[str, Any],
    *,
    retrieved_at: Any,
    source_url: str,
) -> list[PublicSignal]:
    """Parse a current API response without backdating public availability.

    USAspending action and modification dates are not publication timestamps.
    A current response is therefore public no earlier than ``retrieved_at`` unless
    a separately archived release establishes an earlier availability time.
    """
    signals = []
    for award in response.get("results", []):
        award_id = award.get("Award ID")
        recipient = award.get("Recipient Name")
        agency = award.get("Awarding Sub Agency") or award.get("Awarding Agency")
        if not award_id or not recipient or not agency:
            raise ValueError("USAspending award lacks ID, recipient, or agency")
        signals.append(
            PublicSignal(
                signal_id=f"usaspending:{award_id}",
                signal_type="government_award",
                focal_entity=recipient,
                related_entity=agency,
                asset_id=None,
                action_date=award.get("Base Obligation Date"),
                amount_usd=award.get("Award Amount"),
                published_at=retrieved_at,
                source_url=source_url,
                availability_precision="retrieval_only",
            )
        )
    return validate_unique_signal_ids(signals)
