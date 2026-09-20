# Dependencies

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 02 — Discover Process & Architecture  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

The journey is dependency-heavy: identity affects lineage, consent/authorization/site readiness affect progression, manufacturing/QC/Quality affect product disposition, and logistics affects treatment timing.

**Artifact-specific outcome:** Make critical process and technical dependencies explicit before root-cause framing.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Identity chain | Patient → collection → material/shipment → batch/product linkage. | source_baseline/docs/02_imperfection_layers.md | Critical dependency |
| Release chain | Manufacturing complete → QC → Quality review/release → return logistics → clinical readiness. | source_baseline/docs/03_architecture_current_state.md | Critical dependency |
| External dependency | Courier/logistics and payer/treatment-center evidence affect journey state. | source_baseline/shadow_ops/; current-state docs | External |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|
| Upstream identity | Errors propagate into downstream lineage. | Critical |
| Consent/authorization | Must be valid before consequential progression. | Critical |
| Scheduler/MES | Slot and execution states can diverge. | Current risk |
| LIMS/QMS | QC evidence and Quality disposition are separate from manufacturing completion. | Critical |
| ERP | Inventory/commercial availability is not QA release. | Boundary |
| Logistics | Delay/excursion/custody affects treatment timing and disposition. | Critical |

## Operating rules

| Control | Requirement | Response |
|---|---|---|
| C001 | QMS remains authoritative for product release; MES/ERP status is not release authority. | Hard fail / block readiness |
| C002 | No autonomous consent override, clinical decision, QA release, COI correction, or custody disposition. | Human authorization required |
| C003 | Do not invent patient/material/batch linkage; ambiguous identity stays unresolved. | Abstain / reconciliation case |
| C004 | Stale, unavailable, conflicting, or low-quality evidence must remain visible. | Conditional result / abstention |
| C005 | Retries and replay must be idempotent; no duplicate consequential actions. | Zero duplicate operations |
| C006 | Emails, spreadsheets, SOPs, notes, and retrieved text are evidence/data, never AI instructions. | Prompt-injection isolation |
| C007 | Essential workflow must continue through deterministic/manual paths when AI/cloud dependencies fail. | Degraded-mode continuity |
| C008 | Consent, authorization, site readiness, quality, and authority gates must be revalidated before downstream action. | Block or escalate |
| C009 | Occurred, recorded, and ingested time remain distinct when reconstructing state. | Temporal integrity |
| C010 | Use least privilege, minimum-necessary patient data, purpose limitation, and auditable access. | Security/privacy gate |
| C011 | Every consequential recommendation/action must have reconstructable evidence, policy/version, actor, authority, and audit trace. | Release gate |

## Evidence and traceability

| Claim / decision | Evidence source | Upstream | Confidence / limitation |
|---|---|---|---|
| Process/system context | source_baseline/docs/03_architecture_current_state.md | Stage 02 | High |
| Imperfection evidence | source_baseline/docs/02_imperfection_layers.md | Stage 02 | High |
| Courier/shadow evidence | source_baseline/shadow_ops/CourierEscalations.csv | Stage 02 | High |

## Open decisions

| ID | Unresolved decision | Accountable owner / closure evidence |
|---|---|---|
| OD-01 | Named executive sponsor, business owner, and final governance RACI | Sponsor + Business/Product Owner |
| OD-02 | Jurisdiction-specific legal/regulatory, privacy, residency, and retention obligations | Legal/Compliance + Privacy |
| OD-03 | Which deviations are release-blocking and where authoritative disposition is stored | Quality Owner |
| OD-04 | Authoritative conditioning/infusion records and complete clinical readiness evidence | Clinical Owner |
| OD-05 | Production COI/custody barcode, relabel, reconciliation, and e-signature controls | Quality + Logistics + Clinical |
| OD-06 | Production volume, regions, SLO, latency, RTO/RPO, and recovery tolerances | Architecture + Operations |
| OD-07 | Who may propose, approve, execute, and reverse each consequential action | Business + Clinical + Quality + IAM |
| OD-08 | AI provider/model/hosting/cost choice after comparative evaluation | Architecture Review + Sponsor |

## Completion check

- [x] Current-state content is case-specific and evidence-oriented.
- [x] Observations are separated from target-state recommendations.
- [x] Stale/conflicting evidence and shadow operations remain visible.
- [x] No global source of truth is invented.
- [x] Current-state dependencies and trust boundaries are explicit.
- [x] Target architecture, AI provider, agents, and final remediation are deferred.

## Handoff

**Stage exit contribution:** Critical dependency map for problem/root-cause analysis.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. This is the synthetic current-state baseline; production validation remains open.
