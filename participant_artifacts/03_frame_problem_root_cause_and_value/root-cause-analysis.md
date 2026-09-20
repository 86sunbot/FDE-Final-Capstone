# Root-Cause Analysis

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 03 — Frame Problem, Root Cause & Value  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

The main problem is not a single bad system; it is fragmented and conflicting evidence combined with weak authority semantics, identity reconciliation, temporal integrity, distributed workflow safety, and shadow operations.

**Artifact-specific outcome:** Trace visible symptoms to evidence-backed systemic causes without prematurely prescribing technology.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| RC-01 Authority semantics | MES/ERP readiness-like states can be confused with QMS release authority. | Stage 02 system landscape | Root cause |
| RC-02 Identity | Cross-system identity and lineage evidence can disagree. | Stage 02 brownfield assessment | Root cause |
| RC-03 Workflow safety | Retries, distributed state, missing compensation/idempotency create operational risk. | Existing code/tests + Stage 02 | Root cause |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Authority conflict | Manufacturing complete, inventory available, and QA released are different business facts. | Supported |
| Identity inconsistency | Duplicate/conflicting identifiers and demographics weaken lineage confidence. | Supported |
| Gate weakness | Consent, authorization, site readiness, and quality gates can be stale or bypassed downstream. | Supported |
| Temporal inconsistency | Event order and timestamps cannot always be trusted as one clock. | Supported |
| Distributed workflow weakness | Retry/timeouts/conflicts can create duplicate or divergent actions. | Supported |
| Shadow operations | Email and spreadsheets compensate for formal-system gaps. | Supported |
| Incomplete events | Event stream alone cannot reconstruct the full journey. | Supported |

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
| Imperfection catalogue | source_baseline/docs/02_imperfection_layers.md | Stage 03 | High |
| Shadow operations | source_baseline/shadow_ops/ | Stage 03 | High |
| Existing code/tests | source_baseline/src/; source_baseline/tests/ | Stage 03 | High for synthetic baseline |
| Legacy data | source_baseline/data/cgt_legacy.db | Stage 03 | Requires query-level reproduction for exact counts |

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

**Stage exit contribution:** Root-cause chain connecting observed brownfield symptoms to the core problem.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. Production baselines and targets require stakeholder validation.
