# Stakeholder and Affected-Groups Map

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 01 — Mandate & Field Immersion  
**Participant status:** `READY_FOR_SPONSOR_REVIEW`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Treat the patient as the primary affected party and map operators, decision authorities, technology teams, and external parties separately so that usability and authority are not confused.

**Artifact-specific outcome:** Create the stakeholder map needed for field discovery, approvals, human oversight, and adoption planning.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Primary affected group | Patients receiving individualized CGT therapy. | Challenge brief context | High consequence |
| Operational users | Coordinators, treatment-center staff, schedulers, manufacturing, QC/QA, logistics, exception teams. | Current-state process | Validate with stakeholder interviews |
| Decision authorities | Clinical, Quality, Manufacturing, Logistics, Security/Privacy, Regulatory. | source_baseline/AGENTS.md | Authority boundary |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|
| Patients | Treatment timing, identity assurance, product traceability, delay risk. | Primary affected group |
| Clinical/Treatment-center staff | Clinical milestones, consent, readiness, infusion coordination. | Operational + authority |
| Manufacturing/Scheduler | Slot capacity, manufacturing execution, recovery/rebooking. | Operational + authority |
| QC/Quality | QC evidence, deviations, release disposition. | Authority |
| Logistics/Couriers | Collection/product shipment, custody, telemetry, escalation. | Operational/external |
| Security/Privacy/Compliance | Data access, permissible use, privacy, legal/regulatory review. | Control functions |
| Technology teams | CRM/Clinical/Scheduler/MES/LIMS/QMS/ERP/Integration/Data/Cloud. | Enablers |
| Payers and external providers | Authorization and external service dependencies. | External |

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
| Current system/process landscape | source_baseline/docs/03_architecture_current_state.md | Stage 01 | High |
| Shadow operational channels | source_baseline/shadow_ops/ | Stage 01 | High |
| Stakeholder names | Not supplied | Stage 01 | Role-level only |

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

- [x] Minimum content is case-specific and usable for the synthetic capstone.
- [x] Material claims point to repository evidence or are labelled assumptions/limitations.
- [x] Conflicting and stale evidence is preserved rather than silently reconciled.
- [x] Human, deterministic, and AI responsibilities are distinguishable.
- [x] No sponsor, legal, clinical, quality, security, or production approval is fabricated.
- [x] Downstream dependencies and unresolved decisions are explicit.

## Handoff

**Stage exit contribution:** Stakeholder and affected-groups baseline.  
**Gate status:** `READY_FOR_SPONSOR_REVIEW`. Formal stakeholder validation remains pending where named above.
