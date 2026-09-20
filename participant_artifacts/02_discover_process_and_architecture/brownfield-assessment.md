# Brownfield Assessment

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 02 — Discover Process & Architecture  
**Participant status:** `INTERNAL_BASELINE_COMPLETE`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

The inherited estate is deliberately imperfect: identity, release semantics, consent/authorization gates, timestamps, retries, shadow operations, event coverage, and demo-grade integration all contain inconsistencies that must be preserved as evidence before redesign.

**Artifact-specific outcome:** Assess the estate through imperfection, inconsistency, friction, complexity, volatility, uncertainty, hidden dependency, and unknown-unknown lenses.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Brownfield seam | Preserve existing source systems and wrap them with evidence-aware integration rather than assume big-bang replacement. | source_baseline/docs/02_imperfection_layers.md | Current-state finding |
| Shadow operations | Spreadsheets, email and courier escalation records are part of the real operating process. | source_baseline/shadow_ops/ | Current-state dependency |
| Technical baseline | Existing Python/API/database/tests are useful for reconstruction but are not production-grade proof. | source_baseline/src/; source_baseline/tests/ | Reuse with caution |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|
| Imperfection | Missing/weak controls, incomplete events, unauthenticated/demo-grade components. | Observed |
| Inconsistency | Identity, release, authorization, timing, slot/state disagreements. | Observed |
| Friction | Manual reconciliation, email escalation, spreadsheet overrides. | Observed |
| Complexity | Individualized patient-material-batch lineage and distributed decision authority. | Inherent |
| Volatility | Slots, logistics, readiness, delays, deviations. | Inherent |
| Uncertainty | Conflicting identity, telemetry, temporal and quality evidence. | Observed |
| Hidden dependency | Release/quality/logistics changes cascade into treatment readiness. | Observed |
| Unknown unknown | Real operational effort, scale, SLA and production failure patterns are not fully supplied. | Open |

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
| Imperfection layers | source_baseline/docs/02_imperfection_layers.md | Stage 02 | High |
| Shadow operations | source_baseline/shadow_ops/ | Stage 02 | High |
| Legacy database | source_baseline/data/cgt_legacy.db | Stage 02 | High; binary data requires query-level verification |
| Existing implementation | source_baseline/src/; source_baseline/tests/ | Stage 02 | High for demo baseline |

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

- [x] Current-state content is case-specific and evidence-oriented.
- [x] Observations are separated from target-state recommendations.
- [x] Stale/conflicting evidence and shadow operations remain visible.
- [x] No global source of truth is invented.
- [x] Current-state dependencies and trust boundaries are explicit.
- [x] Target architecture, AI provider, agents, and final remediation are deferred.

## Handoff

**Stage exit contribution:** Evidence-backed brownfield risk and friction baseline.  
**Gate status:** `INTERNAL_BASELINE_COMPLETE`. This is the synthetic current-state baseline; production validation remains open.
