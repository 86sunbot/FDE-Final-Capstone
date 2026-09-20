# KPI Tree

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 03 — Frame Problem, Root Cause & Value  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Organize metrics under four business outcomes: safety, speed, operational efficiency, and reliability/traceability.

**Artifact-specific outcome:** Connect technical and workflow improvements to measurable business outcomes.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Safety | Identity exceptions, unauthorized actions, unresolved conflicts. | Stage 02 findings | Business outcome |
| Speed | Vein-to-vein time, avoidable delay, open-exception age. | Capstone baseline | Business outcome |
| Efficiency | Manual reconciliation, manual updates, slot utilization. | Capstone baseline | Business outcome |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Safer journey | Identity exceptions; unsafe/unauthorized actions; unresolved critical conflicts. | KPI branch |
| Faster journey | Median vein-to-vein time; avoidable delay; exception age. | KPI branch |
| More efficient operations | Manual reconciliation; manual status updates; slot utilization. | KPI branch |
| More reliable operations | On-time infusion; traceability completeness; replay safety. | KPI branch |
| Better prediction | QA-release forecast MAE where forecasting is used. | KPI branch |

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
| Business problem | source_baseline/docs/01_problem_context.md | Stage 03 | High |
| Existing requirements/traceability | requirements/requirements.csv; requirements/TRACEABILITY_MATRIX.csv | Stage 03 | High for current capstone implementation |
| Baseline figures | supplied capstone assessment / prior verified analysis | Stage 03 | Synthetic; production validation pending |

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

**Stage exit contribution:** Business-to-operational KPI hierarchy.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. Production baselines and targets require stakeholder validation.
