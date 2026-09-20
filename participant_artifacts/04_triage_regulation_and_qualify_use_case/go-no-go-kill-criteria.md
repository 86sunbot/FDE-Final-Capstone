# Go / No-Go / Kill Criteria

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 04 — Triage Regulation & Qualify Use Case  
**Participant status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Proceed with an AI capability only when the task benefits from unstructured synthesis, the output is evidence-grounded and verifiable, human authority remains intact, and measurable value exceeds risk. Suspend it when those conditions fail.

**Artifact-specific outcome:** Turn AI enthusiasm into explicit entry, rejection, and suspension rules.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| GO | Verifiable evidence-grounded output; human oversight; measurable value; safe fallback. | Stage 03 CTQs/value hypothesis | Required |
| NO-GO | AI becomes final authority, output cannot be verified, deterministic logic is safer, or risk outweighs value. | Stage 04 suitability | Required |
| KILL/SUSPEND | Fabricated evidence, unauthorized action, repeated injection success, unsafe over-trust, unacceptable security/cost/value result. | Counter-metrics + RAI | Required |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| GO | Unstructured evidence synthesis materially reduces operator effort. | Criterion |
| GO | Output cites current/allowed evidence and can be checked. | Criterion |
| GO | Human decision owner remains clear. | Criterion |
| NO-GO | AI can release product or override consent/clinical/identity/custody authority. | Hard no-go |
| NO-GO | Critical control is better implemented deterministically. | Hard no-go |
| KILL | Fabricated source/evidence above accepted threshold. | Suspend |
| KILL | Unauthorized consequential action or hidden critical conflict. | Suspend |
| KILL | Prompt injection repeatedly crosses control boundary. | Suspend |
| KILL | Business value is negligible or cost/risk is unacceptable. | Stop/reshape |

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
| CTQs/counter-metrics | participant_artifacts/03_frame_problem_root_cause_and_value/ctqs.md; counter-metrics.md | Stage 04 | Internal artifacts |
| Repository authority rules | source_baseline/AGENTS.md | Stage 04 | High |
| Verification matrix | requirements/verification_matrix.csv | Stage 04 | High |

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

**Stage exit contribution:** Explicit AI go/no-go/kill gate.  
**Gate status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`. Real stakeholder/legal approval remains pending.
