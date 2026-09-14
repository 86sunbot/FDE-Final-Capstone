# Stage 2 - Brownfield Assessment Through Eight Lenses

**Status:** Evidence-backed internal assessment; domain-owner review pending  
**Evidence source:** `01_REPRODUCIBLE_FORENSIC_BASELINE.md` and `forensic_baseline.json`  
**Last updated:** 2026-09-14

## Executive finding

The brownfield problem is not a single bad release rule or missing AI assistant. It is an inability to combine source-specific evidence into a trustworthy, time-aware and authority-aware journey decision. Multiple systems describe different aspects of reality, while legacy code, spreadsheets and emails turn partial evidence into apparently definitive operational status.

The target must therefore be an evidence and orchestration layer, not a falsely centralized “single source of truth.”

## Lens 1 - Imperfection

**Question:** What is technically or operationally wrong?

### Evidence

- `F-READY-003`: The legacy heuristic reports 499 journeys ready, while 153 are not QMS released, 30 lack valid consent, 205 lack approved authorization, 145 depend on expired/due site controls, seven have confirmed/cancelled slot conflict and 243 lack a delivered return shipment. Categories overlap.
- `F-QUALITY-002`: All 188 deviation links fail to resolve to the event stream: 36 blank and 152 nonblank missing IDs.
- `F-INTEG-001`: Seven retry-duplicate manufacturing-start events exist.
- Legacy `SlotService.reserve` creates a new reservation on every retry and exposes no idempotency key.
- The legacy excursion rule implements superseded SOP-LOG-007 v6 and returns safe for missing temperatures.
- SQLite tables contain weak types and no primary keys, foreign keys, not-null rules or migrations.

### Root issue

Business invariants, identity, time, authority and distributed-command semantics are not encoded as enforceable shared controls.

### Required response

Explicit state machines, typed contracts, fail-closed gates, immutable evidence, idempotent commands, constraint-backed persistence and tests written before defect repair.

## Lens 2 - Inconsistency

**Question:** Which sources, states or rules contradict each other?

### Evidence

- `F-IDENT-001` through `F-IDENT-005`: two duplicate MRNs, ten DOB differences, twelve treatment-center differences, seven MRN differences and 21 name/alias differences across CRM/clinical evidence.
- `F-READY-001`: Sixteen batches are MES `RELEASED` while QMS is not released.
- `F-READY-002`: 158 batches are ERP `AVAILABLE` while QMS is not released.
- `F-READY-004`: 73 `INFUSED` and 32 `INFUSION_READY` patients have product whose QMS state is not released.
- `F-TIME-001`: Nine shipments arrive before departure.
- `F-INTEG-002`: Nine slots are scheduler `CONFIRMED` and MES `CANCELLED`.
- `F-SHADOW-001`: 523 formal/shadow patient priorities disagree.
- `F-LOG-001`: 398 `BOOKED`/`IN_TRANSIT` shipments already have arrival timestamps.
- Release/version metadata refers inconsistently to v1 and v2.

### Root issue

Source-specific meanings are conflated into shared strings without attribute-level authority, reconciliation or temporal context.

### Required response

Canonical semantics, source/attribute authority matrix, evidence-bearing assertions, conflict cases, bitemporal projections and visible uncertainty.

## Lens 3 - Friction

**Question:** Where is unnecessary human or manual effort occurring?

### Evidence

- `F-SHADOW-001`: 523 priority disagreements require reconciliation.
- `F-SHADOW-002`: Twelve slot rows contain planner notes outside governed transactions.
- `F-SHADOW-003`: Sixty emails carry 17 slot moves, 12 courier-route issues, 14 identity reconciliations, seven QA exceptions and ten site-readiness warnings.
- `F-SHADOW-004`: 31 courier escalations include 21 open and eight unowned cases.
- The current API exception view covers open deviations only and excludes other exception domains.

### Root issue

The formal systems do not support a closed-loop cross-domain exception workflow with ownership, evidence, authority, SLA and outcome.

### Required response

Unified exception/case management, accountable ownership, prioritized queues, evidence summaries, approvals, resolution records and operational telemetry.

## Lens 4 - Complexity

**Question:** What remains difficult even when the software works correctly?

### Evidence

- One patient journey spans clinical, payer, treatment-center, logistics, manufacturing, laboratory, Quality and commercial contexts.
- `F-QUALITY-001`: 135 deviations remain open/investigating, including 39 critical; 74 coexist with released QMS state.
- `F-QUALITY-003`: 283 released batches contain at least one pending/OOS/OOT assay row, requiring disposition context rather than naive rejection.
- Effective logistics SOP v7 requires duration, sensor quality, cumulative profile, shipper integrity and Quality review.
- Capacity, patient readiness, product viability and conditioning dependencies change over a journey lasting days or weeks.

### Root issue

Many decisions require multiple time-dependent evidence sources and domain authority. Complexity cannot be removed by normalizing status strings or adding an LLM.

### Required response

Domain decomposition, explicit decision models, evidence lineage, policy versioning, human review and simulations for disruption/capacity trade-offs.

## Lens 5 - Volatility

**Question:** What keeps changing dynamically?

### Evidence

- `F-TIME-002`: Ten patient histories change apparent sequence when ordered by recorded rather than occurred time.
- `F-TIME-003`: Event recording lag reaches 12 hours.
- Slots, routes, qualification, payer authorization, lab queues, deviations and patient readiness can change after an earlier decision.
- Failure scenarios include apheresis delay, suite outage, assay backlog, courier disruption, QMS outage and authorization withdrawal.

### Root issue

The current estate stores snapshots and status strings without robust versioning, revalidation, compensation or late-event handling.

### Required response

Bitemporal events, versioned projections, optimistic concurrency, dependency revalidation, sagas, compensation and bounded planning horizons.

## Lens 6 - Uncertainty

**Question:** What cannot be known with complete confidence?

### Evidence

- Identity sources disagree and lack adjudication evidence.
- `F-QUALITY-003`: Non-pass QC values coexist with released state but no explicit disposition trail explains whether they block release.
- `F-THERMAL-001`: Nineteen shipments are flagged, sixteen have a point above -120 C, three are flagged without such a point, ten temperature values are missing and 27 carry warning quality.
- `F-TIME-003`: Late-recorded events can alter a journey reconstruction.
- Email and spreadsheet statements may be stale, incomplete or adversarial.

### Root issue

The estate collapses unknown, conflicting, missing and not-applicable information into ordinary values or implicit assumptions.

### Required response

First-class uncertainty, confidence, evidence sufficiency, abstention, human escalation, data-quality metadata and no fabricated identity/lineage links.

## Lens 7 - Hidden dependency

**Question:** What downstream consequence is not immediately visible?

### Evidence

- Consent contains 44 expired versions and five withdrawals.
- Authorization contains five denied, 166 pending and 161 conditional cases.
- `F-SITE-001`: Six centers have expired training or due equipment.
- `F-READY-002`: ERP availability hides missing QMS release for 158 batches.
- Slot, courier and site emails are not linked to formal workflow state.
- Conditioning and infusion readiness depend on product release, arrival/viability and clinical authorization not represented together.

### Root issue

Local system status does not encode cross-domain prerequisites or revalidation triggers.

### Required response

Dependency graph/decision model, attribute-level authority, versioned gates, impact analysis and alerts when upstream evidence invalidates downstream plans.

## Lens 8 - Unknown unknown

**Question:** What has the enterprise never modelled or measured?

### Evidence

- `F-EVENT-001`: Only eight event types exist. Consent, authorization, site qualification, slot confirmation, QC, deviation, QA release, conditioning and infusion are missing as first-class events.
- There is no measured human override/rejection rate, exception age by type, cost per successful resolution, data-provenance completeness, automation-bias indicator or recovery-objective performance.
- Unowned escalations and offline workarounds may not be fully represented by the supplied files.
- No telemetry proves which current status users actually trust or how often they bypass formal systems.

### Root issue

The organization has not instrumented the complete decision and exception lifecycle.

### Required response

Observability designed around business decisions, ownership, workarounds, uncertainty, human behavior, value and recovery—not only technical availability.

## Cross-lens priority assessment

| Priority | Problem cluster | Principal evidence | Why now |
|---|---|---|---|
| P0 | Identity, COI and evidence integrity | F-IDENT-001..005 | Wrong or invented linkage can affect an individualized therapy |
| P0 | Product release/readiness semantics | F-READY-001..004; F-QUALITY-001..003 | Manufacturing/ERP/journey status can appear safe without complete Quality evidence |
| P0 | Consent, authorization and site gates | F-GATE-001..002; F-SITE-001 | Hidden prerequisites can invalidate downstream progression |
| P0 | Human authority and audit | Source code/API review and challenge constraints | Current baseline exposes no enforceable approval boundary |
| P1 | Temporal/event reconstruction | F-TIME-001..003; F-EVENT-001 | Late, missing and contradictory events undermine journey state |
| P1 | Distributed command integrity | F-INTEG-001..002 | Retry and partial failure can duplicate or strand capacity actions |
| P1 | Shadow exception operations | F-SHADOW-001..004 | Critical decisions are manual, fragmented and sometimes unowned |
| P1 | Thermal/logistics adjudication | F-THERMAL-001; F-LOG-001 | Evidence quality and SOP context are missing from disposition logic |
| P2 | Packaging and delivery maturity | version drift, weak schemas/tests | Reduces reproducibility and confidence but follows safety remediation |

## Stage 2 conclusion

The highest-value intervention is a deterministic, evidence-bearing orchestration and exception layer with explicit authority. AI is potentially useful for extracting candidate facts, summarizing evidence, explaining impact and proposing alternatives. AI is not justified for identity resolution, gate decisions, deviation closure, release, disposition or other consequential mutations.
