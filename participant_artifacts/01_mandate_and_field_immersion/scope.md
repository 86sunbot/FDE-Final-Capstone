# Scope

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 01 — Mandate & Field Immersion  
**Participant status:** `READY_FOR_SPONSOR_REVIEW`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Scope the engagement across the patient-to-batch-to-infusion-readiness journey and the evidence needed to reconstruct it. Exclude transfer of Clinical/Quality authority, big-bang source replacement, and premature technology selection.

**Artifact-specific outcome:** Create a clear business, system, data, and authority boundary for discovery.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Business boundary | Patient identification/enrolment through infusion readiness. | source_baseline/participant/CHALLENGE_BRIEF.md | In scope |
| System boundary | Clinical/CRM, consent/payer, scheduler, MES, LIMS, QMS, ERP, logistics, sensors, shadow operations, APIs/events. | source_baseline/docs/03_architecture_current_state.md | In scope |
| Exclusions | Autonomous consequential decisions; global system-of-record replacement; model/provider selection. | source_baseline/AGENTS.md | Out of scope now |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|
| In scope — process | Identity, eligibility, consent, authorization, site readiness, collection, COI/custody, logistics, manufacturing, QC, QA release, return logistics, conditioning/infusion readiness. | Addressed |
| In scope — evidence | Database, raw/reference data, SOPs, emails, spreadsheets, contracts, code, tests, events, scenarios. | Addressed |
| In scope — concerns | Authority, identity, temporal integrity, stale/conflicting evidence, retries, exception handling, traceability. | Addressed |
| Out of scope now | Provider choice, final target architecture, autonomous release/consent/clinical decisions, full enterprise redesign. | Addressed |

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
| Journey scope | source_baseline/participant/CHALLENGE_BRIEF.md | Stage 01 | High |
| System landscape | source_baseline/docs/03_architecture_current_state.md | Stage 01 | High |
| Data map | source_baseline/docs/05_data_map.md | Stage 01 | High |

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

**Stage exit contribution:** Agreed discovery scope and boundaries.  
**Gate status:** `READY_FOR_SPONSOR_REVIEW`. Formal stakeholder validation remains pending where named above.
