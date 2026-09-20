# Non-AI Alternative

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 04 — Triage Regulation & Qualify Use Case  
**Participant status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

A strong non-AI solution can address much of the core problem using a canonical evidence model, deterministic state/gate engine, conflict detection, workflow orchestration, audit, and an operator dashboard.

**Artifact-specific outcome:** Prove that AI is optional and must add incremental value on top of deterministic controls.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Evidence layer | Normalize observations while preserving source, time, authority, conflict, and provenance. | Stage 02 findings | Deterministic |
| Gate/state layer | Apply versioned rules for consent, authorization, readiness, quality, release, and authority. | Stage 03 CTQs | Deterministic |
| Workflow layer | Idempotent commands, exception queue, compensation, audit, human approval. | Stage 02 distributed-workflow findings | Deterministic |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Journey projection | Reconstruct evidence-backed patient/material/batch state. | Non-AI |
| Conflict detection | Flag identity/state/time/authority contradictions. | Non-AI |
| Readiness gates | Evaluate versioned business rules. | Non-AI |
| Exception queue | Route unresolved cases to authorized humans. | Non-AI |
| Orchestration | Safe reserve/rebook/retry/compensate with audit. | Non-AI |
| Dashboard | Present state, evidence, blockers, ownership. | Non-AI |
| AI increment | Optional summarization/explanation/prioritization/forecasting. | Separate evaluation |

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
| Non-prescribed solution principle | source_baseline/docs/04_target_capabilities_not_prescribed_solutions.md | Stage 04 | High |
| Brownfield problem | source_baseline/docs/02_imperfection_layers.md | Stage 04 | High |
| Requirements | requirements/requirements.csv | Stage 04 | High |

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

**Stage exit contribution:** Conventional baseline against which AI must prove incremental value.  
**Gate status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`. Real stakeholder/legal approval remains pending.
