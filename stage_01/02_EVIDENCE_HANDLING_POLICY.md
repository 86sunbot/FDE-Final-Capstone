# Stage 1 - Evidence Handling and Source-of-Truth Policy

**Status:** Effective for capstone work; stakeholder review pending  
**Last updated:** 2026-09-14

## 1. Purpose

Preserve the challenge estate as admissible engineering evidence while allowing reproducible analysis and safe POC development.

## 2. Evidence baseline

| Attribute | Value |
|---|---|
| Evidence ID | EVD-001 |
| File | `/Users/suryap/Documents/FDE/Capstone/AI_FDE_CGT_Patient_to_Batch_Orchestration.zip` |
| Size | 992,289 bytes |
| Filesystem modification time | 2026-09-10T20:07:40+05:30 |
| ZIP entries | 132 |
| SHA-256 | `74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979` |
| Internal checksum manifest | 130 files listed; 130 verified; 0 missing; 0 mismatched |
| Data classification | Fully synthetic training/challenge evidence |
| Preservation state | Original remains in place; no write performed |

## 3. Authority hierarchy

No individual operational data source is assumed to be the global source of truth.

| Priority | Source type | Authority and use |
|---:|---|---|
| 1 | User mandate and approved decisions | Defines project intent, scope and authorization |
| 2 | Challenge brief and discovery checklist | Defines required capstone outcomes and discovery questions |
| 3 | Controlled synthetic source evidence | Supports or contradicts operational facts; conflicts must be preserved |
| 4 | SOPs and documented business rules | Define rule intent subject to version, scope and human authority |
| 5 | Executable legacy code and contracts | Evidence of implemented behavior, not necessarily correct business truth |
| 6 | Tests and diagnostics | Evidence only within their verified coverage |
| 7 | AntiGravity prototype and earlier reports | Candidate reusable material; claims require independent verification |
| 8 | Codex-generated artifacts | Derived analysis or implementation; never primary evidence by themselves |

## 4. Handling zones

### Zone A - Immutable source evidence

- The original ZIP.
- Never edited, reformatted, renamed, repacked or used as a mutable runtime database.
- Integrity verified by SHA-256 before major analysis milestones and at final closeout.

### Zone B - Verified extracted baseline

- A byte-identical extraction created from Zone A for analysis.
- Treated as read-only by process.
- Compared against the ZIP and internal checksum manifest.
- Not used for destructive workflow demonstrations.

### Zone C - Working fixtures

- Explicit copies derived from Zone B.
- May be migrated or mutated by POCs and tests.
- Each copy records source hash, creation method, schema version and test purpose.
- Disposable and reproducible.

### Zone D - Derived evidence and outputs

- Queries, profiles, findings, diagrams, specifications, code, tests and reports.
- Every material claim links back to Zone A/B evidence or is labelled assumption/hypothesis.

## 5. Required evidence metadata

Every material finding must record:

- Evidence ID.
- Source path and source system.
- Table, record, line, query or function reference.
- Extraction or query method.
- Observed fact.
- Interpretation.
- Confidence and uncertainty.
- Applicable legacy lens.
- Potential impact.
- Required human/domain validation.
- Related requirement, ADR, test and KPI when created.

## 6. Conflict policy

- Preserve conflicting values and their provenance.
- Do not overwrite one source with another to make data appear consistent.
- Do not invent identity, patient, collection, shipment, batch or product links.
- Use explicit states such as `UNRESOLVED`, `CONFLICTING` and `UNKNOWN` where appropriate.
- Resolution must record the evidence considered, resolver identity, authority, time and reason.

## 7. Temporal policy

Events and decisions must distinguish:

- `occurred_at`: when the physical or business event occurred.
- `recorded_at`: when a source system recorded it.
- `ingested_at`: when the orchestrator received it.
- `effective_from/effective_to`: when a rule or fact is valid, where applicable.

Late, duplicate and out-of-order events remain observable.

## 8. Working-data policy

- Runtime code must never point to Zone A or B databases for mutation.
- Tests create temporary databases or fixture copies.
- Baseline and working databases must have different paths and explicit names.
- Test teardown removes only test-owned files.
- Idempotent regeneration instructions are required.

## 9. Generated-claim policy

Use the following labels:

- **FACT:** directly supported by verified evidence.
- **MEASUREMENT:** produced by a reproducible method with source and time.
- **INFERENCE:** reasoned from evidence but not directly observed.
- **ASSUMPTION:** accepted temporarily and awaiting confirmation.
- **HYPOTHESIS:** proposed future outcome to test.
- **TARGET:** desired threshold, not achieved performance.
- **GAP:** missing or insufficient evidence.

## 10. Approval and audit

- Codex may verify hashes, analyze copies and produce derived artifacts.
- Only authorized stakeholders may approve clinical, Quality, privacy, regulatory or lifecycle conclusions.
- Integrity verification results are recorded in the progress log.
- The original ZIP hash is rechecked before final delivery.
