# Prohibited / Unacceptable Use Check

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 04 — Triage Regulation & Qualify Use Case  
**Participant status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Autonomous AI must not exercise Clinical, Quality, consent, identity/COI, custody, or other consequential authority in this capstone. It must also not bypass access or safety controls.

**Artifact-specific outcome:** Define unacceptable AI use before model/provider selection or implementation.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| QA release | AI may summarize evidence but may not release/disposition product. | source_baseline/AGENTS.md | Prohibited autonomous use |
| Consent/clinical | AI may surface status/evidence but may not override consent or make clinical decisions. | source_baseline/AGENTS.md | Prohibited autonomous use |
| Identity/COI/custody | AI may flag ambiguity but may not invent/correct authoritative lineage or custody. | Stage 03 CTQs | Prohibited autonomous use |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Autonomous QA release | Rejected. | Hard boundary |
| Consent override | Rejected. | Hard boundary |
| Clinical treatment decision | Rejected. | Hard boundary |
| Patient/material identity correction without human authority | Rejected. | Hard boundary |
| COI/custody disposition | Rejected. | Hard boundary |
| Authorization/RBAC bypass | Rejected. | Hard boundary |
| Autonomous retry/compensation based on model judgment | Rejected; use deterministic workflow. | Hard boundary |
| Use of restricted patient data outside approved purpose | Rejected. | Hard boundary |

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
| Repository authority rules | source_baseline/AGENTS.md | Stage 04 | High |
| Security/privacy context | source_baseline/docs/06_security_privacy_assurance.md | Stage 04 | High |
| CTQs | participant_artifacts/03_frame_problem_root_cause_and_value/ctqs.md | Stage 04 | Internal artifact |

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

- [x] Non-AI and AI approaches are compared.
- [x] Consequential actions are excluded from autonomous AI authority.
- [x] Regulatory relevance is separated from confirmed legal classification.
- [x] Human oversight and verification are explicit.
- [x] Go/no-go/kill conditions are defined.
- [x] No provider/model or target architecture is selected at this stage.

## Handoff

**Stage exit contribution:** Explicit prohibited/unacceptable AI-use boundary.  
**Gate status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`. Real stakeholder/legal approval remains pending.
