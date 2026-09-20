# Value / Risk / Feasibility Matrix

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 04 — Triage Regulation & Qualify Use Case  
**Participant status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Prioritize evidence summarization and exception explanation for POC evaluation; treat prioritization and forecasting as test candidates; reject autonomous identity/release/consent/retry decisioning.

**Artifact-specific outcome:** Compare candidate AI use cases on value, risk, and feasibility before architecture selection.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| High-priority candidate | Evidence summarization and exception explanation. | Stage 04 suitability | Proceed to eval design |
| Conditional candidate | Grounded Q&A, case prioritization, delay/ETA forecasting. | Stage 04 suitability | Test first |
| Rejected candidate | Autonomous identity resolution, QA release, consent override, retry orchestration. | CTQs/prohibited-use check | Reject |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Evidence summarization | Value: High; Risk: Medium; Feasibility: High. | Proceed |
| Exception explanation | Value: High; Risk: Medium; Feasibility: High. | Proceed |
| Grounded SOP/evidence Q&A | Value: Medium/High; Risk: Medium; Feasibility: High. | Conditional |
| Case prioritization | Value: Medium/High; Risk: Medium; Feasibility: Medium. | Test |
| Delay/ETA forecasting | Value: High; Risk: Medium; Feasibility: Medium. | POC candidate |
| Identity auto-resolution | Value: Medium; Risk: Very High; Feasibility: Medium. | Reject autonomous |
| QA release automation | Incremental value: Low; Risk: Very High. | Reject |
| AI retry handling | Value: Low; Risk: High; deterministic alternative superior. | Reject |

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
| Value hypothesis | participant_artifacts/03_frame_problem_root_cause_and_value/value-hypothesis.md | Stage 04 | Internal |
| CTQs/counter-metrics | participant_artifacts/03_frame_problem_root_cause_and_value/ctqs.md; counter-metrics.md | Stage 04 | Internal |
| Existing verification evidence | requirements/verification_matrix.csv | Stage 04 | High for capstone |

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

**Stage exit contribution:** Prioritized candidate-use-case portfolio for Stage 07/08 evaluation and option selection.  
**Gate status:** `CONDITIONAL_GO_FOR_SYNTHETIC_POC`. Real stakeholder/legal approval remains pending.
