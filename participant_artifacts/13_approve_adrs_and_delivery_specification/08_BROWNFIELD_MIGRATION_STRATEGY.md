# Brownfield Migration, Coexistence, Cutover and Rollback Strategy

**Status:** Design for the synthetic capstone; enterprise execution requires source owners and a new approval gate
**Decision:** Evidence-layer strangler migration, not a big-bang master-data replacement
**Related:** Stage 5 context map; Stage 10 C4; ADR-001/004/007/011; Stage 17 local shadow/canary exercise

## 1. Migration objective and boundary

Keep CRM, clinical, scheduler, MES, LIMS, QMS, ERP, logistics, payer and controlled human procedures as their own sources of assertions and decision authority. Add a read-only evidence layer first. Rebuild a canonical journey projection from source-specific facts, policy versions and authorized decisions without overwriting contradictory source records. Introduce consequential commands only after source contracts, human authority, idempotency, reconciliation and compensation are tested with accountable owners.

The current `source_baseline` is a frozen synthetic fixture, not a live enterprise connection. Local shadow/canary runs compare fixed POC fixtures; they are not a dual-run with production systems.

## 2. Source-by-source coexistence plan

| Source boundary | Read-only first increment | Decision owner and semantic rule | Command/cutover condition |
|---|---|---|---|
| CRM enrollment | Namespace-qualified CRM identifiers, aliases, recorded time | CRM owns enrollment assertion, not final clinical identity | Never auto-merge; approved reconciliation contract first |
| Clinical and treatment center | Subject/MRN/DOB, eligibility, consent, site milestones | Clinical authority owns clinical milestones; conflicts remain open | Authenticated identity/consent decision and audit first |
| Payer/authorization | Status, version, effective time and revocation | Payer source asserts financing; downstream milestone policy is separate | Revalidate before consequential downstream step |
| Collection/COI/COC | Collection, bag, label and custody evidence edges | Identity/collection authority must attest any disputed relationship | No write until scan/attestation and correction protocol exists |
| Scheduler and shadow slot files | Planned slot, scheduler/MES disagreement, human override history | Planner may propose; scheduler/MES acknowledgements remain distinct | Payload-bound command ledger, query-before-retry, compensation |
| MES and ERP | Manufacturing and inventory assertions | MES completion and ERP availability never imply Quality release | Source adapters are read-only for POC |
| LIMS and QMS | QC, deviation, SOP version, explicit authorized release event | Quality/QP alone owns release/disposition; missing evidence is `UNKNOWN` | Validated e-signature and controlled policy before live release flow |
| Courier, shipment and sensors | Custody/status, occurred/recorded time, unit/sensor quality | Logistics assertion is not disposition authority | Alternative route requires human approval and carrier contract |
| Email/spreadsheets | Historical shadow evidence with locator and age | Untrusted operational notes, never executable instruction | Replace only after owner has accepted new case/exception workflow |

## 3. Sequenced migration waves

| Wave | Entry | Work | Evidence/exit | Reversal |
|---|---|---|---|---|
| M0 - freeze and profile | Verified v2 checksums | Preserve raw fixtures and source contracts; profile identities, relationships, status/time/unit conflicts | Reproducible baseline and issue register | No source write; stop extraction |
| M1 - read-only assertions | M0 plus approved field/purpose map | Ingest namespaced assertions with locator, digest, occurred and recorded time; quarantine invalid schema/units | Source-to-assertion lineage and reconciliation counts | Disable adapter; rebuild from source |
| M2 - shadow projection | M1 and controlled milestone policy | Calculate journey/readiness with uncertainty; compare against source/manual view without affecting actions | Paired scenario differences, false-ready/false-block review, owner sign-off | Turn off projection/UI; source workflow unchanged |
| M3 - owned exceptions | M2 and operational RACI | Route conflicts, stale facts, outage and delays to named queues with evidence packets | No unowned P0; case aging and handoff tests | Fall back to existing documented exception procedure |
| M4 - controlled commands | M3 and IAM/signature/contract tests | Start with low-risk slot command adapter; require semantic idempotency, outbox/inbox, reconciliation, compensation, audit | Zero duplicate effects and blind retries under fault/concurrency cases | Stop outbound dispatch, reconcile ledger, return to legacy procedure |
| M5 - bounded canary | M4 and independent G4/G5 approval | Pilot a limited site/product/cohort under dual-run and bounded authorities | Human study, contract/load/DR, safety and benefit gates | Feature flag off, drain/reconcile in-flight commands, restore legacy ownership |
| M6 - expansion/decommission | M5 real measured outcomes | Expand by country/site only with regulatory/privacy/Quality and supplier decisions; retire shadow work after adoption evidence | Signed cutover and records-retention/hold plan | Cohort-specific backout; never erase source/audit history |

Only M0 and limited M1/M2-style synthetic demonstrations are authorized by this capstone. M3-M6 describe a future accountable program, not work completed here.

## 4. Backfill, dual-run and cutover rules

- Backfill imports source assertions as historical facts with original source/effective/occurred/recorded fields. Unknown time is not invented; import time is a separate platform field.
- Each identifier retains source namespace and relationship evidence. A same-string MRN or COI is not an automatic link.
- A batch or journey projection is rebuildable; source records and approved decision events are never destructively replaced.
- Dual-run compares identical named cohorts and milestone policy versions. Every mismatch has an owner, evidence packet and disposition; a headline percentage cannot hide P0 discrepancies.
- Cutover is a per-workflow/per-site decision, not one global flag. Entry requires controlled policies, source-owner contracts, human training, signed authority, replay/load/DR, incident procedure and independent assurance.
- Outbound commands carry correlation, actor, idempotency key and payload digest. An unknown acknowledgement blocks retry until the target system is queried and the outcome is reconciled.
- Rollback stops new commands first, reconciles in-flight effects, verifies audit/event state, and then returns work to the documented legacy owner. A database restore cannot undo an external command.

## 5. Acceptance matrix and open owners

| Gate | Required evidence | Accountable owner hypothesis | Current state |
|---|---|---|---|
| Source contract and permissible use | Contract tests, field map, retention/privacy decision | Source Owner + Privacy/Data Owner | Synthetic fixture only |
| Identity/COI mapping | Independent golden decisions and correction protocol | Clinical/Identity Authority | Missing |
| Slot command cutover | Scheduler sandbox, idempotency/partial-effect tests | Manufacturing Planner + Platform Owner | Local simulator only |
| Release/Quality interface | Controlled QC/deviation/thermal policy and validated signature | Quality/QP | Missing; no live release allowed |
| Shadow-case adoption | Training, owner acceptance and workaround log | Operations Service Owner | Missing |
| Safety and resilience | Full scenario TEVV, 20-client load, restore/DR and security tests | Independent Assurance + SRE | Internal local tests only |
| Scale decision | Real before/after KPI, counter-metrics and regional applicability | Sponsor/Product Owner | Not measured |

This strategy is intentionally reversible and evidence-preserving. It cannot be approved for a real cutover by Codex or by an academic simulation.
