# Critical to Quality (CTQs)

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 03 — Frame Problem, Root Cause & Value  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

The solution is acceptable only if identity/lineage, release authority, journey-state derivation, traceability, retry safety, and human authority remain correct under normal and degraded conditions.

**Artifact-specific outcome:** Translate the business problem into non-negotiable quality characteristics.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| CTQ-01 Identity | Do not fabricate patient/material/batch links. | Stage 02 identity findings | Non-negotiable |
| CTQ-02 Release | QMS authority must be respected. | Stage 02 system/authority map | Non-negotiable |
| CTQ-03 Journey state | Readiness must be evidence-derived, conflict-aware, and versioned. | Stage 02 data-flow findings | Non-negotiable |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|---|
| Correct identity/lineage | Ambiguity creates reconciliation case, not guessed linkage. | CTQ |
| Correct release authority | Manufacturing/ERP states never substitute for QA release. | CTQ |
| Evidence-backed state | Every derived status points to source evidence and rule/policy version. | CTQ |
| Traceability | Important claims and actions are reconstructable. | CTQ |
| Safe retries | Idempotent handling prevents duplicate consequential actions. | CTQ |
| Human authority | Consequential decisions remain with authorized roles. | CTQ |
| Degraded mode | System fails safe and preserves manual/deterministic continuity. | CTQ |

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
| Repository safety rules | source_baseline/AGENTS.md | Stage 03 | High |
| Imperfection layers | source_baseline/docs/02_imperfection_layers.md | Stage 03 | High |
| Security/privacy assurance | source_baseline/docs/06_security_privacy_assurance.md | Stage 03 | High |

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

**Stage exit contribution:** Quality characteristics that later architecture, tests, and evals must satisfy.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. Production baselines and targets require stakeholder validation.
