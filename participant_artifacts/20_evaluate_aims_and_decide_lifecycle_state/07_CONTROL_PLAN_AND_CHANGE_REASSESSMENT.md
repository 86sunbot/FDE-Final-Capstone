# Academic Control Plan and Change Reassessment

**Status:** Internal synthetic POC control plan; not a validated organizational AIMS
**Lifecycle state:** `RESTRICT_AND_CHANGE`; AI off; no real patient/workflow or consequential external adapter

| Control | Trigger/frequency | Evidence | Response/owner hypothesis |
|---|---|---|---|
| Frozen source integrity | Every evidence rebuild/release | ZIP and 132-file digest inventory | Stop on mismatch; Evidence Owner investigates |
| P0 authority and identity/Quality gates | Every code/policy change | Negative and normal tests; requirement verification matrix | Block release on failure; Domain/Quality owners review |
| Idempotency/unknown outcomes | Every command-adapter change | Replay/concurrency/fault tests; reconciliation ledger | Disable dispatch; Planner/Platform Owner reconciles |
| Source schema/time/unit/relationship drift | Every future adapter ingest | Source contract and quarantine counts | Stop affected projection; Source/Data Owner resolves |
| AI output boundary | Every mode/model/provider/prompt change | Structured-output, citation, injection, fallback tests | AI off immediately; deterministic service continues |
| Case ownership and audit integrity | Every drill and release | P0 owner count, audit hash-chain test, incident records | Isolate mutation path; Operations/Security review |
| Recovery | Before any pilot and after storage change | Backup/replay/restore digest; measured RTO/RPO | No pilot without independent DR acceptance |
| Human oversight/automation bias | Before any real pilot | Controlled role study and override rationale | Keep advisory/restricted if inconclusive |
| Value and counter-metrics | At each gate and monthly after real pilot | Approved baseline/after formulas; false-block and burden metrics | No ROI or scale claim without observed data |

Changes to intended purpose, country/site/cohort, patient data, authority, clinical/Quality policy, model/provider, integration contract, source truth, signature reliance, or deployment topology require a new impact/risk/applicability review before implementation. The accountable owner must update Stage 4, 7, 10, 12, 13 and 15 artifacts, run all affected P0 cases, and record a fresh gate decision. Codex internal review is not independent acceptance.

The 90-day roadmap and open CAPA owners are in `06_PRODUCTION_GAP_AND_90_DAY_ROADMAP.md`. An academic simulation can exercise controls but cannot close real-world CAPAs.
