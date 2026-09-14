# Stage 3 - SCQA and Prioritized Problem Statement

**Status:** Evidence-backed draft  
**Inputs:** Stage 2 verified baseline and brownfield assessment  
**Last updated:** 2026-09-14

## 1. SCQA

### Situation

The simulated enterprise coordinates individualized autologous Cell and Gene Therapy journeys across clinical sites, collection, Chain of Identity/Custody, cryogenic logistics, manufacturing capacity, manufacturing execution, QC, QA release, return logistics and infusion readiness. The estate has enough functioning software and data to support many ordinary journeys.

### Complication

The difficult journeys cross independently evolved sources whose identifiers, statuses, timestamps, rules and operational decisions disagree. Legacy code converts manufacturing or ERP status into product readiness; critical prerequisites such as consent, authorization, site controls, Quality evidence and return delivery are omitted. Late and duplicate events, partial slot transactions, broken deviation links and shadow spreadsheets/email weaken traceability and recovery. No shared control establishes evidence sufficiency, uncertainty, accountable authority or a closed-loop exception outcome.

### Question

How can the enterprise create a trustworthy, explainable and resilient patient-to-batch operational view and coordinate cross-system action without erasing source disagreement, fabricating identity/lineage, or transferring consequential authority to AI?

### Answer hypothesis

Introduce an incremental, evidence-preserving orchestration and exception layer that:

1. Maintains source-specific facts and bitemporal provenance.
2. Reconstructs one canonical domain/decision model without declaring one global database authoritative.
3. Enforces deterministic identity, consent, site, authorization, state, idempotency and Quality gates.
4. Routes uncertainty and consequential action to authenticated humans.
5. Uses bounded AI only to extract candidate facts, summarize evidence, explain impact and recommend alternatives.
6. Measures safety, traceability, flow, human workload, resilience and cost before recommending a pilot.

This answer remains a hypothesis until Stages 7, 8 and 15 compare it with non-AI alternatives and verify it.

## 2. Concise problem statement

The brownfield estate cannot reliably determine or explain end-to-end patient/product readiness because source-specific evidence, time, domain semantics, distributed actions and decision authority are fragmented. This creates unsafe derived states, manual reconciliation, unowned exceptions, duplicate/conflicting actions and weak recovery. The capstone must prove a deterministic, auditable orchestration foundation and test whether bounded AI improves exception work without increasing risk or automation bias.

## 3. Prioritized problem register

| Priority | Problem | Evidence | Consequence | Deterministic need | Potential AI role |
|---|---|---|---|---|---|
| P0 | Identity and lineage conflicts lack governed reconciliation | F-IDENT-001..005 | Wrong or unprovable individualized-therapy association | Evidence graph/assertions, matching constraints, cases and approval | Summarize conflicting evidence; never merge autonomously |
| P0 | Product readiness conflates MES, ERP, QMS and journey state | F-READY-001..004 | Premature downstream readiness | Versioned decision model and hard Quality-authority gate | Explain blockers/evidence; no release action |
| P0 | Consent, authorization and site dependencies are omitted | F-GATE-001..002; F-SITE-001 | Invalid scheduling or clinical progression | Milestone-specific deterministic prerequisites and revalidation | Summarize impact/escalation options |
| P0 | Consequential human authority is documentary, not enforced | Baseline API/code and challenge constraints | Role spoofing or autonomous mutation | Authentication, authorization, signatures and separation of duties | No authority; recommendation only |
| P1 | Quality evidence lacks blocking/disposition/event semantics | F-QUALITY-001..003 | Delay, unnecessary hold or unsafe interpretation | Blocking classification, disposition state and evidence links | Assemble/summarize review packet |
| P1 | Event time, recording time and current state are not governed | F-TIME-001..003; F-EVENT-001 | Stale or incorrect journey projection | Bitemporal envelope, replay and correction policy | Explain changes and uncertainty |
| P1 | Cross-system commands lack idempotency and compensation | F-INTEG-001..002 | Duplicate reservation, lost capacity or unknown recovery | Command ledger, inbox/outbox, concurrency, saga and compensation | Rank safe alternatives after deterministic simulation |
| P1 | Exceptions are fragmented across email/CSV and may be unowned | F-SHADOW-001..004 | Slow, inconsistent and unaudited resolution | Case lifecycle, ownership, SLA, escalation and audit | Extract candidate facts, summarize and prioritize |
| P1 | Logistics/thermal evidence lacks contextual adjudication | F-THERMAL-001; F-LOG-001; SOP v7 | False alarm or unsafe viability assumption | Typed telemetry, duration/quality/profile calculation and Quality approval | Evidence summary and decision support only |
| P2 | Forecasting and optimization are weak or absent | Supplied KPI baseline and failure scenarios | Avoidable delay and inefficient capacity | Measured baseline and constraint model first | ETA, risk and alternative ranking if evaluation proves value |
| P2 | Platform and delivery controls are demonstration-grade | Code/contracts/tests/version drift | Low reproducibility and assurance | Contracts, migrations, CI/CD, observability and SLOs | Developer assistance only |

## 4. Prioritization method

Problems are ordered using:

1. Potential patient/individualized-product safety impact.
2. Consequential decision authority.
3. Frequency and breadth in the supplied evidence.
4. Ability to propagate across downstream dependencies.
5. Reversibility and detectability.
6. Manual burden and delay.
7. Feasibility of a testable capstone intervention.

No numerical risk score is claimed here. Stage 7 will establish the formal impact/likelihood methodology and risk acceptance.

## 5. Scope decision

The capstone will focus on three vertical problem slices:

- Patient/identity readiness.
- Manufacturing disruption and slot orchestration.
- Product/QA/thermal-release support.

These slices cover all P0 problems and representative P1 problems while remaining locally testable. Full enterprise replacement, clinical decision automation and production integration remain out of scope.
