# Stage 6 - Data Quality Profile and Issue Register

**Status:** Reproduced technical profile; business interpretation pending  
**Last updated:** 2026-09-14

## 1. Quality dimensions

The assessment separates completeness, uniqueness, syntactic validity, referential integrity, semantic consistency, temporal coherence, provenance and representativeness. Passing one dimension does not establish business truth.

## 2. Structural results

| Check | Result | Correct interpretation |
|---|---:|---|
| Declared profile-key duplicate groups across 23 CSVs | 0 | File keys are unique under the declared profiling keys; MRN still has two duplicate groups because MRN is not a safe global key |
| Invalid declared temporal values | 0 | Nonblank profiled dates/times parse syntactically; nine shipment sequences remain physically impossible |
| Invalid declared numeric values | 0 | Selected typed candidates parse; SQLite still stores every column as `TEXT` |
| Cross-file relationship checks | 25 | Broad technical coverage of declared references |
| Relationship issues | 188 | All are unresolved deviation-to-event links; no other declared reference check failed |
| Event ID duplicate groups | 0 | Transport IDs are unique |
| Semantic retry duplicates | 7 | Unique event IDs do not provide business idempotency |
| Event types | 8 | Event coverage is materially incomplete for the journey/control lifecycle |
| Maximum recording lag | 12 hours | Late evidence must be represented, not silently reordered |

## 3. Contextual null analysis

| Field | Blank count | Interpretation |
|---|---:|---|
| Telemetry `temperature_c` | 10 | Genuine missing sensor values; quality is `MISSING` and must remain visible |
| Deviation `linked_event_id` | 36 | Missing evidence linkage; another 152 nonblank values also fail to resolve |
| QC `unit` | 3,200 | Structural for the four textual assays in this synthetic schema; not automatically a defect, but the value representation is polymorphic/weakly typed |
| Outbound shipment `batch_id` | 800 | Structurally expected before manufacturing batch creation; direction-specific constraint needed |
| Courier escalation `owner` | 8 | Operational accountability defect |
| Shadow slot `planner_note` | 788 | Optional note; the 12 nonblank notes reveal workaround decisions |
| Shadow priority `reason` | 640 | Weak decision rationale/provenance for 80% of shadow priorities |

Null counts are not summed into a generic quality score because their meanings differ.

## 4. Data-quality issue register

| ID | Dimension | Severity | Measured evidence | Impact | Required handling |
|---|---|---|---|---|---|
| DQ-001 | Identity consistency | P0 | 2 duplicate MRN groups; 10 DOB, 12 center, 7 MRN and 21 name/alias disagreements | Wrong or unprovable patient association | Source-specific assertions; conflict case; authorized resolution |
| DQ-002 | Decision semantics | P0 | 16 MES/QMS and 158 ERP/QMS release conflicts | Premature readiness | Separate execution, inventory and Quality decision models |
| DQ-003 | Referential integrity | P1 | 188/188 deviation links unresolved | Quality evidence cannot be reconstructed | Preserve broken link; resolve only from evidence; no fabricated event |
| DQ-004 | Temporal coherence | P1 | 9 shipments arrive before departure; 10 histories invert by recorded order | Wrong projection/causal interpretation | Bitemporal event model and conflict case |
| DQ-005 | Event completeness | P1 | Only 8 event types | Consent, authorization, site, slot, QC, deviation, release and approval history absent | Add target events; do not reconstruct unsupported history as fact |
| DQ-006 | Semantic uniqueness | P1 | 7 duplicate manufacturing-start facts with unique IDs | Duplicate action/effect risk | Semantic fingerprint and idempotent command ledger |
| DQ-007 | Telemetry completeness/quality | P1 | 10 missing values; 27 warnings | Thermal profile uncertainty | Typed observations; approved quality/profile calculation; Quality review |
| DQ-008 | Snapshot consistency | P1 | 398 non-delivered statuses already have arrival time | Physical/status state conflict | Source assertion plus receipt/custody event; open case |
| DQ-009 | Quality disposition semantics | P0 | 283 QMS-released batches with pending/OOS/OOT rows | Unsafe or false adverse conclusion without disposition | Obtain required assay/blocking/disposition evidence |
| DQ-010 | Site-control consistency | P1 | 6 centers with expired training or due equipment despite higher-level status | Hidden readiness dependency | Attribute-level rule and time-bound qualification |
| DQ-011 | Shadow decision provenance | P1 | 523 priority disagreements; 640 blank reasons; 8 unowned escalations | Reconciliation, fairness and accountability risk | Owned case/decision history and rationale |
| DQ-012 | Schema enforcement | P1 | SQLite columns all `TEXT`; no PK/FK/not-null constraints | Invalid units/types/relations can enter unnoticed | Target typed contracts and migrations; source remains unchanged |
| DQ-013 | Version metadata consistency | P2 | v1 repo metadata within v2 package | Reproduction/configuration ambiguity | Bind every artifact to hash and explicit source/package version |
| DQ-014 | KPI reproducibility | P1 | 10 supplied baseline formulas absent | Benefit claims cannot be independently reproduced | Define populations/formulas or retain `PROVIDED_NOT_REPRODUCED` |

## 5. Quality acceptance rules for target ingestion

- Never drop or overwrite a raw source value during normalization.
- Reject/quarantine records missing mandatory envelope fields.
- Represent missing, invalid, warning and conflicting separately.
- Apply direction/type-specific optionality rather than global null rules.
- Use typed identifiers, quantities and units in canonical contracts.
- Validate declared references but do not treat matching strings as independent identity/COI proof.
- Open a case when a P0 conflict cannot be resolved deterministically.
- Record transformation code/version, input/output hashes and counts.
- Reconcile late/corrected events through append-only bitemporal processing.

## 6. Fitness conclusion

The data is fit for synthetic forensic analysis, deterministic rule/state-machine engineering and controlled POC evaluation. It is conditionally fit for evaluating evidence summarization if prompt data remains synthetic and ground-truth rubrics are added. It is not fit to prove autonomous decisions, real-world predictive accuracy, clinical effectiveness, product disposition or production compliance.
