# Use-Case Card — Governed Readiness and Exception Copilot

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 04 — Triage Regulation & Qualify Use Case  
**Participant status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Qualify a bounded copilot that reconstructs gate state from deterministic evidence, explains blockers, summarizes relevant evidence, and recommends next actions while authorized humans own consequential decisions.

**Artifact-specific outcome:** Select a focused AI-assisted use case that addresses manual interpretation without transferring authority.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| User | Operations/clinical/quality/logistics coordinators handling journey exceptions. | Stage 01 stakeholder map | Primary user group |
| AI task | Summarize blockers/evidence/uncertainty, answer grounded questions, recommend next step. | Stage 04 suitability | Advisory only |
| Deterministic dependency | Gate state, authority, identity, freshness, and action permissions are computed outside the model. | Non-AI alternative | Mandatory |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Problem | Operators spend time reconstructing why a journey is blocked across conflicting sources. | Supported |
| Inputs | Journey evidence, QC/deviation, consent/auth, logistics, email/SOP context subject to access policy. | Bounded |
| AI contribution | Summarize, explain, compare, draft/recommend. | Allowed |
| Human role | Review evidence and make/approve consequential decision. | Required |
| AI boundary | No release, override, identity correction, custody disposition, or unauthorized tool action. | Hard boundary |
| Value | Reduce triage/reconciliation time and improve explanation/traceability. | Hypothesis |
| Evaluation | Groundedness, citation correctness, blocker accuracy, abstention, injection resistance, operator value. | Stage 07 dependency |

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
| Stage 03 problem frame | participant_artifacts/03_frame_problem_root_cause_and_value/scqa-problem-frame.md | Stage 04 | Internal |
| Requirements | requirements/requirements.csv | Stage 04 | High |
| Safety rules | source_baseline/AGENTS.md | Stage 04 | High |

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

**Stage exit contribution:** Capstone-qualified governed readiness/exception copilot use case.  
**Gate status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`. Real stakeholder/legal approval remains pending.
