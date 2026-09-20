# Value Hypothesis

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 03 — Frame Problem, Root Cause & Value  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

If teams receive an evidence-backed journey view, explicit authority-aware gates, early exception detection, and safe cross-system coordination, manual reconciliation and avoidable delay should fall while traceability and on-time treatment performance improve.

**Artifact-specific outcome:** State a testable value hypothesis with measurable outcomes and counter-metrics.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Value mechanism | Better evidence/state reconstruction reduces time spent discovering what is true. | Stage 02 waste register | Hypothesis |
| Operational mechanism | Explicit gates and exception ownership reduce unsafe or late progression. | Stage 02 dependencies | Hypothesis |
| Safety mechanism | Deterministic authority/identity controls prevent optimization from overriding critical safeguards. | CTQs/counter-metrics | Required |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Expected benefit | Lower manual reconciliation. | Testable |
| Expected benefit | Lower avoidable delay and exception age. | Testable |
| Expected benefit | Higher traceability and on-time journey performance. | Testable |
| Expected benefit | Better slot/use of operational capacity. | Testable |
| Counter-effect to avoid | More hidden conflict, unsafe automation, privacy risk, duplicate action, or operator over-trust. | Guarded |
| Production claim | None; synthetic POC must not be presented as production ROI proof. | Explicit |

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
| Waste/friction | participant_artifacts/02_discover_process_and_architecture/waste-register.md | Stage 03 | Internal artifact |
| Requirements | requirements/requirements.csv | Stage 03 | High |
| Problem context | source_baseline/docs/01_problem_context.md | Stage 03 | High |

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

- [x] Context, symptoms, problem, root causes, and impact are separated.
- [x] Baselines are distinguished from proposed targets.
- [x] Value is tied to measurable operational outcomes.
- [x] Counter-metrics protect safety, authority, and traceability.
- [x] Causation is not claimed where evidence only supports correlation.
- [x] No target architecture or AI provider choice is introduced.

## Handoff

**Stage exit contribution:** Testable business value hypothesis for option evaluation and pilots.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. Production baselines and targets require stakeholder validation.
