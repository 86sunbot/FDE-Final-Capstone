# Sponsor and Owner Model

**Case:** CGT Patient-to-Batch Orchestration Capstone  
**Stage:** 01 — Mandate & Field Immersion  
**Participant status:** `READY_FOR_SPONSOR_REVIEW`  
**Evidence cut:** 2026-09-20 private repository snapshot; synthetic source baseline  
**Approval note:** Internal FDE/capstone artifact. Named sponsor, Clinical, Quality, Legal/Compliance, Security/Privacy and production approvals are not implied.

## Decision / outcome

Use role-based ownership in the synthetic capstone and keep all named production owners as TBD rather than fabricating identities.

**Artifact-specific outcome:** Identify the owner roles required to approve scope, business value, clinical/quality decisions, privacy/security, and production operation.

## Specification

| Element | Decision / requirement | Evidence | Status / boundary |
|---|---|---|---|
| Executive sponsor | Owns mandate, funding, escalation, and final scale/change/stop decision. | Challenge brief context | Name TBD |
| Business/Product owner | Owns business outcome and operational acceptance. | Challenge brief context | Name TBD |
| Domain owners | Clinical, Quality, Manufacturing, Logistics, Security/Privacy, Regulatory/Compliance, Operations. | source_baseline/AGENTS.md | Roles required |

## Required content coverage

| Required field | Case-specific answer | Disposition |
|---|---|---|
| Executive Sponsor | Accountable for engagement mandate and investment decision. | TBD |
| Business/Product Owner | Accountable for measurable business outcome. | TBD |
| FDE Lead | Responsible for discovery, design, evidence traceability, engineering coordination. | Participant role |
| Clinical Owner | Accountable for clinical milestones/readiness decisions. | TBD |
| Quality Owner | Accountable for release/deviation authority. | TBD |
| Manufacturing Owner | Accountable for manufacturing execution decisions. | TBD |
| Logistics Owner | Accountable for shipment/custody operations. | TBD |
| Security/Privacy Owner | Accountable for access, privacy, data use controls. | TBD |
| Regulatory/Compliance Owner | Accountable for legal/regulatory interpretation. | TBD |
| Operations Owner | Accountable for production service ownership. | TBD |

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
| Required authority separation | source_baseline/AGENTS.md | Stage 01 | High |
| Real names | Not supplied in synthetic repository | Stage 01 | Unknown |

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

**Stage exit contribution:** Role-based sponsorship and ownership model.  
**Gate status:** `READY_FOR_SPONSOR_REVIEW`. Formal stakeholder validation remains pending where named above.
