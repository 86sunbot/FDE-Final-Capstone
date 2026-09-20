# AI Suitability Assessment

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 04 — Triage Regulation & Qualify Use Case  
**Participant status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

AI is suitable only for bounded, evidence-grounded assistance such as summarization, explanation, prioritization, and forecasting. Identity, consent, authorization, release authority, permissions, retries, and audit remain deterministic and/or human-authorized.

**Artifact-specific outcome:** Approve advisory AI only where outputs are verifiable and errors do not directly exercise consequential authority.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Suitable | Evidence summarization, exception explanation, grounded operational Q&A, selected prioritization/forecasting. | Stage 03 problem/value frame | Conditional go |
| Unsuitable | QA release, consent override, identity/COI correction, custody disposition, clinical decisions, retry control. | source_baseline/AGENTS.md | No-go |
| Verification | AI outputs must cite evidence and expose uncertainty; human reviews consequential recommendations. | requirements/verification_matrix.csv | Required |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Evidence summarization | High suitability; unstructured and human-verifiable. | Proceed to evaluation |
| Exception explanation | High suitability; cross-source synthesis adds value. | Proceed to evaluation |
| SOP/evidence Q&A | Medium/High if grounded and version-aware. | Conditional |
| Case prioritization | Medium; must remain explainable and bounded. | Test |
| Delay forecasting | Medium; needs calibration, drift monitoring, and advisory use. | POC candidate |
| Identity auto-resolution | Low; consequence too high. | Reject autonomous use |
| QA release/consent/clinical authority | Unacceptable for autonomous AI. | Reject |
| Retry/idempotency handling | Poor AI fit; deterministic engineering is safer. | Deterministic |

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
| Safety/authority rules | source_baseline/AGENTS.md | Stage 04 | High |
| Security/privacy context | source_baseline/docs/06_security_privacy_assurance.md | Stage 04 | High |
| Requirements/evals | requirements/requirements.csv; requirements/verification_matrix.csv | Stage 04 | High for capstone |

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

**Stage exit contribution:** Evidence-backed AI suitability boundary.  
**Gate status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`. Real stakeholder/legal approval remains pending.
