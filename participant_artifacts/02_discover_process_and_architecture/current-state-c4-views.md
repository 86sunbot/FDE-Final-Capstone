# Current-State C4 Views

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 02 — Discover Process & Architecture  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Represent the current estate as a system-of-systems supporting a patient-specific journey. The current-state C4 view must show clinical, scheduling, manufacturing, quality, ERP, logistics and shadow channels without implying a target design.

**Artifact-specific outcome:** Use C4 to expose people, systems, dependencies and boundaries, not to prescribe the future solution.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Context view | Patient/treatment center interacts with enterprise clinical, manufacturing, quality and logistics systems. | source_baseline/docs/03_architecture_current_state.md | Current state |
| Container view | Existing API/database/code components may be shown only as demo/brownfield implementation. | source_baseline/src/ | Current technical baseline |
| Shadow channels | Email/spreadsheets appear as operational dependencies across the formal flow. | source_baseline/shadow_ops/ | Must be visible |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|
| People | Patient, coordinators, clinical, manufacturing, quality, logistics, support teams. | Addressed |
| Systems | CRM/Clinical, consent/payer, scheduler, MES, LIMS, QMS, ERP, logistics/sensors. | Addressed |
| Shadow channels | Email, spreadsheets, manual reconciliation/escalation. | Addressed |
| Trust boundaries | Treatment center, enterprise, manufacturing, courier/external service zones. | Addressed |
| Target C4 | Explicitly deferred. | Correctly deferred |

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
| Current architecture narrative | source_baseline/docs/03_architecture_current_state.md | Stage 02 | High |
| Data map | source_baseline/docs/05_data_map.md | Stage 02 | High |
| Shadow channels | source_baseline/shadow_ops/ | Stage 02 | High |

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

**Stage exit contribution:** Current-state C4 context/container baseline.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. This is the synthetic current-state baseline; production validation remains open.
