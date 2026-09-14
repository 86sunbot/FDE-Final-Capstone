# Stage 1 - Stakeholder and Affected-Groups Map

**Status:** Proposed role map; named owners pending confirmation  
**Last updated:** 2026-09-14

## 1. Governance stakeholders

| Stakeholder role | Primary interest | Required decisions | Evidence needed |
|---|---|---|---|
| Executive Sponsor | Safety, scale, investment and strategic outcome | Mandate, funding, pilot/lifecycle decision | Value, risk, readiness and residual-risk package |
| Capstone Owner | Successful, defensible capstone delivery | Scope, priorities, review and final acceptance | Traceability, working demo and assessment rubric |
| AI FDE Architect / Codex | Evidence analysis, architecture, implementation and verification | Technical recommendations only | Source evidence, requirements, ADRs and test results |
| Product Owner | User value, workflow and backlog | Priorities and acceptance criteria | Journey maps, KPI tree and user feedback |
| Clinical Operations SME | Patient readiness and treatment-site workflow | Clinical-process rules and identity escalation | Patient journey, consent, authorization and site evidence |
| Quality / Qualified Person | QA release, deviations, disposition and GxP evidence | Quality rules and consequential approvals | QMS, QC, SOP, audit and signature evidence |
| Manufacturing Operations | Capacity, batch progression and recovery | Manufacturing and slot operating rules | MES, capacity, scheduling and disruption evidence |
| Logistics Operations | Chain of Custody, routing and cold chain | Logistics rules and escalation paths | Shipment, courier and telemetry evidence |
| Data Owner / Steward | Data definitions, access, quality and lineage | Data meaning, quality acceptance and permissible use | Inventories, profiles, lineage and provenance |
| Security and Privacy | Identity, authorization, PHI and threat controls | Security/privacy acceptance | Threat model, access matrix, DLP and test evidence |
| Regulatory / Legal | Regulatory applicability, records and supplier obligations | Applicability and legal interpretation | Intended purpose, records scope, contracts and assessments |
| Platform / SRE / Service Owner | Reliability, deployment, monitoring and recovery | Operational acceptance | SLOs, runbooks, telemetry and chaos results |
| Independent Assurance Reviewer | Objective challenge of evidence and controls | Independent assurance conclusion | Release candidate, evaluation pack and residual risks |

## 2. Operational participants

| Group | Role in journey | Primary needs | Primary risks from poor orchestration |
|---|---|---|---|
| Patients | Source and recipient of individualized therapy | Correct identity, timely treatment, consent and transparent escalation | Identity error, delay, inappropriate progression or lost opportunity |
| Caregivers/families | Support patient journey | Clear, timely communication | Confusion, missed readiness changes or avoidable burden |
| Treatment-center coordinators | Coordinate eligibility, collection, conditioning and infusion | Reliable cross-system readiness and exception visibility | Manual reconciliation, stale status and unsafe scheduling |
| Apheresis teams | Collect patient material | Correct patient/collection identity and confirmed downstream capacity | Collection mismatch, wasted procedure or chain break |
| Courier teams | Transport cryogenic material/product | Clear custody, route, timing and escalation instructions | Delay, lost custody evidence or unreviewed excursion |
| Manufacturing planners | Allocate scarce slots | Idempotent booking, priorities, constraints and alternatives | Double booking, stranded capacity or unfair prioritization |
| Manufacturing operators | Execute personalized batch processing | Correct material/batch identity and legal sequencing | Wrong-material processing or invalid state progression |
| QC laboratory staff | Produce assay evidence | Complete samples, lineage, methods and result status | Mislinked, delayed or misunderstood results |
| QA/QP reviewers | Review deviations and release evidence | Complete, attributable and contemporaneous evidence | Premature release, weak auditability or authority spoofing |
| Supply-chain planners | Manage disruptions end to end | Impact analysis, alternatives and human control | Automation bias, untracked workaround or cascading delay |
| Reimbursement teams/payers | Provide financial authorization | Correct authorization dependency and status | Treatment scheduled without funding or preventable delay |
| Technology support teams | Operate participating systems | Clear ownership, observability and recovery procedures | Silent failure, drift and prolonged outage |

## 3. Vulnerable or indirectly affected groups

- Patients with urgent clinical timelines.
- Patients whose identity records conflict across systems.
- Patients at sites with expiring or expired qualification.
- Patients with language, accessibility or digital-support needs.
- Operations staff exposed to automation bias or alert fatigue.
- Smaller treatment centers with lower technical capacity.
- External partners subject to data-sharing, jurisdiction or connectivity constraints.

## 4. Engagement approach

| Stage | Engagement needed |
|---|---|
| 1-4 | Confirm mandate, real operating assumptions, affected groups, risks and authority |
| 5-8 | Validate vocabulary, decisions, data fitness, evaluations and solution choice |
| 9-13 | Review architecture, contracts, permissions, controls and build specification |
| 14-16 | Exercise workflows, evaluate human factors, test recovery and approve procedures |
| 17-20 | Review shadow/canary evidence, adoption, outcomes, risks and lifecycle decision |
| 21 | Confirm closure, disposition and reusable-IP boundaries |

## 5. Current limitation

No named enterprise stakeholders were provided with the synthetic challenge. The role map is therefore an explicit proposed operating model, not evidence of actual stakeholder interviews or approval.
