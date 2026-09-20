# Counter-Metrics

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 03 — Frame Problem, Root Cause & Value  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Efficiency improvements are unacceptable if they increase identity error, unauthorized release/action, hidden conflicts, duplicate actions, privacy exposure, or operator over-trust.

**Artifact-specific outcome:** Define metrics that must not deteriorate while delay and manual effort are reduced.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Safety counter-metric | Unauthorized consequential actions = 0 in POC/acceptance tests. | source_baseline/AGENTS.md | Hard gate |
| Identity counter-metric | Fabricated patient/material/batch links = 0. | Stage 02 identity findings | Hard gate |
| Retry counter-metric | Duplicate reservations/actions under replay = 0. | Stage 02 brownfield findings | Hard gate |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Unauthorized QA/clinical/consent/COI actions | Must remain zero. | Kill criterion |
| Hidden unresolved identity conflict | Must remain zero; conflict must stay visible. | Kill criterion |
| Duplicate consequential action | Must remain zero under retries/replay. | Kill criterion |
| Traceability completeness | Must not fall while automation increases. | Guard metric |
| Privacy/security incidents | Must not increase due to broader AI/data access. | Guard metric |
| Human override/abstention | Must remain available where uncertainty exists. | Guard metric |

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
| Authority guardrails | source_baseline/AGENTS.md | Stage 03 | High |
| Security/privacy context | source_baseline/docs/06_security_privacy_assurance.md | Stage 03 | High |
| Brownfield risk | source_baseline/docs/02_imperfection_layers.md | Stage 03 | High |

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

**Stage exit contribution:** Safety and quality counter-metrics for value evaluation.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. Production baselines and targets require stakeholder validation.
