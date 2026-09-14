# Stage 1 - Governance RACI and Decision Rights

**Status:** Proposed; human owners and approvers pending confirmation  
**Last updated:** 2026-09-14

## 1. Role abbreviations

| Code | Role |
|---|---|
| ES | Executive Sponsor |
| CO | Capstone Owner |
| FDE | AI FDE Architect / Codex |
| PO | Product Owner |
| CLN | Clinical Operations SME |
| QA | Quality / Qualified Person |
| MFG | Manufacturing Operations |
| LOG | Logistics Operations |
| DATA | Data Owner / Steward |
| SEC | Security and Privacy |
| REG | Regulatory / Legal |
| OPS | Platform / SRE / Service Owner |
| IA | Independent Assurance Reviewer |

## 2. Stage-level RACI

`A` = Accountable, `R` = Responsible, `C` = Consulted, `I` = Informed.

| Stage/workstream | ES | CO | FDE | PO | CLN | QA | MFG | LOG | DATA | SEC | REG | OPS | IA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Mandate and scope | A | R | R | C | C | C | I | I | I | C | C | I | I |
| 2 Brownfield discovery | I | A | R | C | C | C | C | C | C | C | C | C | I |
| 3 Problem/KPI framing | C | A | R | R | C | C | C | C | C | I | I | I | I |
| 4 Regulatory/use-case triage | I | C | R | C | C | A | I | I | C | C | A | I | C |
| 5 Domain model | I | C | R | A | C | C | C | C | C | I | I | I | I |
| 6 Data/knowledge readiness | I | C | R | C | C | C | C | C | A | C | C | I | I |
| 7 Evaluations/risks | I | C | R | C | C | A | C | C | C | C | C | C | C |
| 8 Option selection | A | R | R | C | C | C | C | C | C | C | C | C | I |
| 9 Information architecture | I | C | R | C | C | C | C | C | A | C | C | C | I |
| 10 AI/application architecture | I | C | R | C | C | C | C | C | C | A | C | C | I |
| 11 Agentic/HITL design | I | C | R | C | C | A | C | C | C | C | C | C | I |
| 12 Security/supplier controls | I | C | R | I | C | C | I | I | C | A | C | C | I |
| 13 Build-ready specification | I | A | R | R | C | C | C | C | C | C | C | C | I |
| 14 Engineering | I | A | R | C | C | C | C | C | C | C | I | C | I |
| 15 Evaluation/internal assurance | I | C | R | C | C | A | C | C | C | C | C | C | C |
| 15 Independent assurance | I | I | C | I | I | C | I | I | I | C | C | I | A/R |
| 16 Operational readiness | I | C | R | I | C | C | C | C | C | C | C | A | C |
| 17 Controlled deployment | I | C | R | C | C | A | C | C | I | C | C | A | I |
| 18 Monitoring/resilience | I | I | R | C | C | C | C | C | C | C | I | A | C |
| 19 Value/decision story | C | A | R | R | C | C | C | C | C | I | I | C | I |
| 20 AIMS/lifecycle decision | A | R | C | C | C | C | C | C | C | C | C | C | C |
| 21 Retirement/IP capture | I | A | R | C | C | C | C | C | C | C | C | R | I |

## 3. Consequential decision rights

| Decision/action | Recommender | Required accountable authority | Codex/AI permission | Evidence required |
|---|---|---|---|---|
| Resolve patient identity conflict | FDE/identity assistant may surface evidence | Clinical Operations under approved identity policy | Recommend only | Source records, match features, conflicts, confidence and resolver record |
| Confirm Chain of Identity/Custody | Orchestrator may validate evidence completeness | Authorized Clinical/Manufacturing/Quality role per procedure | Validate and flag only | Scans/events, provenance, timestamps and exception record |
| Accept consent/authorization readiness | Deterministic rules | Clinical Operations | Execute approved deterministic rule only | Current consent/authorization, effective dates, provenance and rule version |
| Approve treatment-site qualification | System may report state | Clinical/Quality owner | No approval | Qualification evidence, effective dates and authority |
| Reserve manufacturing slot | Orchestrator may execute after policy checks | Manufacturing Planner or approved deterministic policy | No autonomous exception override | Capacity, priority, idempotency, constraints and actor identity |
| Resolve scheduling conflict | AI may propose alternatives | Manufacturing/Supply-chain Planner | Recommend only | Conflicts, alternatives, trade-offs and impact |
| Accept thermal disposition | AI may summarize profile and recommend review | Quality / QP | Recommend only | Raw telemetry, quality, duration, shipper integrity, SOP version and review |
| Close deviation | System may present workflow | Quality-authorized individual | Prohibited | Deviation evidence, investigation, reason and electronic signature |
| Release batch/product | System may evaluate prerequisites | QP/authorized Quality role | Prohibited | Manufacturing, QC, deviations, release record and electronic signature |
| Begin conditioning | System may compute readiness | Authorized Clinical role | Prohibited as AI action | Released product, arrival/viability, patient readiness and clinical authorization |
| Override safety gate | None by default | Explicitly authorized human under approved exception procedure | Prohibited | Dual authorization where required, reason, evidence and audit |
| Change AI autonomy | Architecture may recommend | Lifecycle management review with QA/Security | Prohibited | Eval results, risk assessment, monitoring and rollback plan |
| Pilot/go-live decision | FDE may recommend | Sponsor + QA + Security + Operations | No approval authority | Release, assurance, operations, adoption and residual-risk evidence |

## 4. Separation-of-duties rules

- The implementer cannot independently approve Quality release or assurance completion.
- A user cannot establish authority by supplying a role string in an API request.
- Recommendation, approval and execution are distinct auditable actions.
- AI/service identities receive least-privilege permissions and cannot impersonate humans.
- Quality records and electronic signatures require controlled identity and non-repudiation design if the use is confirmed in Part 11 scope.
- Independent assurance must be performed by a reviewer outside the implementation responsibility.

## 5. Pending appointments

Named individuals for all human roles are not available in the synthetic challenge. Before any stage is marked `APPROVED`, the Capstone Owner must either assign a named reviewer or explicitly approve the role-based simulation for academic assessment.
