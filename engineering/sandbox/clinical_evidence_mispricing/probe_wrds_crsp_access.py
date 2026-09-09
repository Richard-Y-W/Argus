"""Non-interactive WRDS readiness probe that never prints credentials."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd

from .crsp_ciz_gate import (
    DAILY_COLUMN_ALIASES,
    HISTORY_COLUMN_ALIASES,
    build_security_link_query,
    credential_status,
    resolve_columns,
)


def audit_schema(*, link_ledger: Path | None = None) -> dict[str, Any]:
    import wrds

    username = os.environ.get("WRDS_USERNAME")
    if not username:
        raise RuntimeError("WRDS_USERNAME is not configured; refusing an interactive prompt")
    connection = wrds.Connection(wrds_username=username)
    try:
        history = connection.describe_table(
            library="crsp", table="stksecurityinfohist"
        )
        daily = connection.describe_table(library="crsp", table="dsf_v2")
        history_columns = resolve_columns(history["name"].tolist(), HISTORY_COLUMN_ALIASES)
        daily_columns = resolve_columns(daily["name"].tolist(), DAILY_COLUMN_ALIASES)
        result: dict[str, Any] = {
            "history_table": "crsp.stksecurityinfohist",
            "daily_table": "crsp.dsf_v2",
            "history_columns": history_columns,
            "daily_columns": daily_columns,
            "ready_for_return_blind_identifier_query": True,
        }
        if link_ledger is not None:
            events = pd.read_csv(link_ledger, dtype={"cik": str})
            required = {"event_ticker", "announcement_date"}
            if not required.issubset(events.columns):
                raise ValueError("event ledger lacks ticker or announcement date")
            query = build_security_link_query(
                table="crsp.stksecurityinfohist",
                columns=history_columns,
                tickers=events["event_ticker"].tolist(),
                start_date=events["announcement_date"].min(),
                end_date=events["announcement_date"].max(),
            )
            links = connection.raw_sql(query)
            result["return_blind_link_rows"] = int(len(links))
            result["return_blind_links"] = links.to_dict(orient="records")
    finally:
        connection.close()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connect", action="store_true")
    parser.add_argument("--link-ledger", type=Path)
    args = parser.parse_args()
    result: dict[str, Any] = {"credential_status": credential_status()}
    if args.connect:
        result["schema_audit"] = audit_schema(link_ledger=args.link_ledger)
    else:
        result["next_step"] = "configure WRDS_USERNAME and a secure WRDS password file, then rerun with --connect"
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
