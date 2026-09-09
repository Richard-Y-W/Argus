# Small-biotech announcement-timing audit

**Status:** return-blind, single-coded timing repair  
**Outcome:** all eight seed rows now have a market-session classification

The initial SEC-supported seed retained four `date_only` rows when its failure evidence came from a retrospective filing. This audit searched for contemporaneous company announcements or SEC acceptance timestamps without opening price histories.

| Event | Timestamp evidence | Classification | Source |
|---|---|---|---|
| SBP3F-002 / VTL | company-issued GlobeNewswire release, 2018-09-12 05:00 ET | pre-market | https://www.globenewswire.com/news-release/2018/09/12/1569553/31568/en/vital-therapies-announces-that-topline-results-of-vtl-308-fail-to-achieve-primary-and-secondary-endpoints-of-improvement-in-survival.html |
| SBP3F-003 / PRTA | event-time SEC accession accepted 2018-04-23 08:01:04 ET; 08:30 conference call | pre-market | https://www.sec.gov/Archives/edgar/data/1559053/000119312518125906/0001193125-18-125906-index-headers.html |
| SBP3F-006 / IMGN | event-time SEC accession accepted 2019-03-01 07:02:12 ET; 08:00 conference call | pre-market | https://www.sec.gov/Archives/edgar/data/855654/000155837019001386/0001558370-19-001386-index-headers.html |
| SBP3F-007 / SAGE | event-time SEC accession accepted 2019-12-05 07:01:03 ET | pre-market | https://www.sec.gov/Archives/edgar/data/1597553/000119312519306717/0001193125-19-306717-index-headers.html |
| SBP3F-008 / TTPH | company-issued GlobeNewswire release, 2018-02-13 16:01 ET | after-market (confirmation) | https://www.globenewswire.com/news-release/2018/02/13/1340188/34757/en/Tetraphase-Announces-Top-Line-Results-from-IGNITE3-Phase-3-Clinical-Trial-of-Eravacycline-in-Complicated-Urinary-Tract-Infections-cUTI.html |

The other three rows were already coded pre-market from event-time primary materials. No row is promoted: exact timestamps and event definitions still require an independent second pass, and the effective-session mapping must use the exchange calendar rather than date arithmetic.
