# Field Evidence Register

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 01 — Mandate & Field Immersion  
**Participant status:** `READY_FOR_SPONSOR_REVIEW`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Treat the repository as a synthetic evidence pack and maintain clear separation between supplied evidence, derived findings, assumptions, stale/conflicting records, and facts that require real stakeholder or production validation.

**Artifact-specific outcome:** Establish the evidence sources that later stages may cite and make evidence limitations visible from the start.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Evidence scope | Challenge brief, discovery checklist, current-state docs, raw/reference data, SQLite, shadow operations, SOPs, contracts, code, tests, evals, and verification outputs. | source_baseline/ | In scope |
| Evidence handling | Preserve contradictions, source authority, time, and version; do not overwrite raw evidence. | source_baseline/docs/02_imperfection_layers.md | Mandatory |
| Field limitation | No real stakeholder interviews or production observations are supplied. | Synthetic training pack | Explicit limitation |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|
| E01 | source_baseline/participant/CHALLENGE_BRIEF.md — engagement mandate | Available |
| E02 | source_baseline/participant/DISCOVERY_CHECKLIST.md — required discovery | Available |
| E03 | source_baseline/data/cgt_legacy.db — legacy operational database | Available |
| E04 | source_baseline/data/raw/ — raw multi-system records | Available |
| E05 | source_baseline/data/reference/ — reference/master-like data | Available |
| E06 | source_baseline/docs/sops/ — SOP/policy evidence | Available |
| E07 | source_baseline/shadow_ops/PatientPriority_MASTER.csv — shadow prioritization | Available |
| E08 | source_baseline/shadow_ops/ManufacturingSlots_FINAL_v7.csv — shadow slot planning | Available |
| E09 | source_baseline/shadow_ops/CourierEscalations.csv — logistics escalations | Available |
| E10 | source_baseline/shadow_ops/emails/ — informal operational evidence | Available |
| E11 | source_baseline/contracts/ — interface/schema evidence | Available |
| E12 | source_baseline/src/ and tests/ — runnable brownfield implementation | Available |
| E13 | source_baseline/evals/ and scenarios/ — evaluation/scenario evidence | Available |
| E14 | Real stakeholder interviews / production observation | Not available |

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
| Synthetic evidence status | source_baseline/LICENSE-SYNTHETIC-TRAINING.txt | Stage 01 | High |
| Source inventory and checksums | source_baseline/data/manifest.json; source_baseline/checksums.sha256 | Stage 01 | High |
| Verification expectations | source_baseline/VERIFICATION.md | Stage 01 | High |

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

- [x] Minimum content is case-specific and usable for the synthetic capstone.
- [x] Material claims point to repository evidence or are labelled assumptions/limitations.
- [x] Conflicting and stale evidence is preserved rather than silently reconciled.
- [x] Human, deterministic, and AI responsibilities are distinguishable.
- [x] No sponsor, legal, clinical, quality, security, or production approval is fabricated.
- [x] Downstream dependencies and unresolved decisions are explicit.

## Handoff

**Stage exit contribution:** Traceable field-evidence baseline for all later stages.  
**Gate status:** `READY_FOR_SPONSOR_REVIEW`. Formal stakeholder validation remains pending where named above.
