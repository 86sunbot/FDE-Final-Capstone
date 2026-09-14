# Stage 9 - Data, Event and Evidence Contracts

**Machine-readable contracts:** `stage_09/contracts/*.schema.json`

## Required event envelope

Every event has event/schema/aggregate identity, sequence, occurred and recorded time, source, evidence references, correlation, actor, data quality, classification, payload digest and trace ID. Authority and policy versions are conditionally required for consequential decisions.

## Contract rules

- Timestamps are timezone-aware ISO 8601.
- IDs are non-empty typed strings; clients cannot change server-issued actor or authority.
- Evidence references resolve to a digest and source locator.
- Payload digest is computed over canonical JSON.
- Unknown, not satisfied and not applicable are distinct.
- A model response is a `Recommendation`, never an event accepted by a state machine.
- Schema changes are additive within a major version; breaking changes require a new version and migration/replay tests.

## Retention and disposition

The academic repository contains synthetic data only. Runtime databases, generated reports and logs are disposable POC data. The immutable challenge ZIP and evidence manifests are retained with checksums. Production retention, legal hold, patient rights, predicate-record and record-signature rules remain unresolved and fail closed.

## Provenance chain

`source locator -> source digest -> assertion/event -> rule version -> projection/decision -> audit record -> evaluation result`

The API returns evidence references for each material fact and blocker. A missing link prevents a P0 assertion from being accepted.
