# CGT Patient-to-Batch Capstone - Master Execution Plan

**Execution status:** COMPLETE FOR SYNTHETIC ACADEMIC POC  
**Final lifecycle decision:** RESTRICT AND CHANGE; real pilot/production not approved

## Purpose

Implement the CGT Patient-to-Batch capstone using Codex and the 21-stage AI FDE Operating Model in [`reference/FDE_PDF.pdf`](../reference/FDE_PDF.pdf).

The capstone will be delivered as an evidence-driven, integrated proof of concept. It must not claim production deployment, regulatory compliance, independent assurance, savings, approval, or legacy retirement without supporting evidence.

## Source baselines

- Original immutable challenge package: `/Users/suryap/Documents/FDE/Capstone/AI_FDE_CGT_Patient_to_Batch_Orchestration.zip`
- FDE framework: the repository copy at [`reference/FDE_PDF.pdf`](../reference/FDE_PDF.pdf); original supplied from `/Users/suryap/Library/Mobile Documents/com~apple~CloudDocs/FDE_PDF.pdf`.
- Existing AntiGravity prototype: `https://github.com/86sunbot/AI-FDE-Capstone-AG`
- Previous repository audit: `/Users/suryap/Documents/Codex/2026-09-11/i/outputs/AntiGravity_Delivery_Recheck_143a48c.md`

The ZIP is evidence and must remain unchanged. The AntiGravity repository is reusable input, not authoritative proof of completion.

## Delivery discipline

Every iteration follows:

`SPECIFY -> BUILD -> VERIFY -> SHIP -> REPEAT`

Every consequential capability must maintain this traceability chain:

`Evidence -> Legacy lens -> Root cause -> Requirement -> ADR -> Implementation -> Test/eval -> KPI -> Lifecycle decision`

## Non-negotiable engineering rules

1. Use one immutable baseline dataset and separate working databases.
2. Do not fabricate evidence, approvals, audits, deployments, compliance, savings, or KPI improvements.
3. Unknown or missing safety information fails closed.
4. AI may summarize evidence and recommend action; it may not independently resolve identity, close deviations, release a batch, or perform other consequential mutations.
5. Authorization is derived from authenticated identity and policy, never from a role supplied in a request body.
6. Domain rules live in shared services, not separately in workflow scripts or user interfaces.
7. Events record both occurrence time and recording time, provenance, schema version, source and confidence where applicable.
8. Safety rules use controlled specifications and typed units. No invented thresholds.
9. Tests must assert business and safety outcomes, not merely successful process exit.
10. All reports distinguish facts, measurements, assumptions, targets, hypotheses and unresolved gaps.

## Programme gates

| Gate | After stage | Decision |
|---|---:|---|
| G1 | 4 | Problem and use case approved |
| G2 | 8 | Solution and trade-offs approved |
| G3 | 13 | Build-ready specification approved |
| G4 | 15 | Release candidate passes internal assurance |
| G5 | 16 | Controlled pilot is operationally ready |
| G6 | 20 | Scale, change, restrict, suspend, or retire |

## Phase 1 - Establish and understand

### Stage 1 - Mandate and field immersion

**Objective:** Establish scope, ownership, affected groups, authority and evidence-handling rules.

**Artifacts:** Engagement charter, scope, outcome statement, stakeholder map, affected-groups map, governance RACI, decision-rights matrix, field-evidence register, Responsible AI context and assumptions log.

**Exit:** Approved mandate and operating context.

### Stage 2 - Discover process and architecture

**Objective:** Establish a reproducible current-state baseline.

**Actions:** Inventory and profile the ZIP; reproduce defects; map the end-to-end journey; inspect systems, data flows, trust boundaries and shadow operations; analyze all findings through Imperfection, Inconsistency, Friction, Complexity, Volatility, Uncertainty, Hidden Dependency and Unknown Unknown.

**Artifacts:** Evidence inventory, evidence queries, SIPOC, value-stream map, waste register, current-state C4 views, system landscape, data flows, dependencies, trust boundaries and brownfield assessment.

**Exit:** Every material finding points to reproducible evidence.

### Stage 3 - Frame problem, root cause and value

**Objective:** Convert evidence into prioritized, measurable problems.

**Artifacts:** SCQA, causal/root-cause analysis, baseline dataset, KPI tree, CTQs, prioritized problem register, value hypotheses, counter-metrics and success/failure criteria.

**Exit:** Root causes, baselines and intended outcomes are measurable.

### Stage 4 - Triage regulation and qualify use case

**Objective:** Bound the regulatory and AI scope.

**Actions:** Assess 21 CFR Part 11 applicability, EU AI Act intended purpose and Article 6 classification, ISO 42001/42005 relevance, privacy, data use, licensing and records obligations. Compare AI with rules-only automation.

**Artifacts:** Applicability screen, prohibited-use check, AI-suitability assessment, non-AI alternative, use-case cards, value-risk-feasibility matrix, go/no-go criteria, kill criteria and authority policy.

**Exit G1:** Approved and justified use case with deterministic and AI boundaries.

## Phase 2 - Model, qualify and select

### Stage 5 - Model the domain

**Objective:** Establish one authoritative business and decision model.

**Artifacts:** Glossary, domain capability map, bounded contexts, context map, aggregates, ownership, business rules, decision tables, domain events and canonical state machine.

**Required properties:** Explicit legal transitions, typed identifiers/units, bitemporal events, provenance and fail-closed unknown states.

**Exit:** Specifications, code and tests can share one vocabulary and state model.

### Stage 6 - Qualify data and knowledge

**Objective:** Determine what information is trustworthy, permitted, representative and usable.

**Artifacts:** Data/knowledge inventory, quality profile, lineage, provenance, access matrix, permissible-use register, representativeness assessment, data-gap register, dataset datasheets, SOP/version register and source trust hierarchy.

**Exit:** Known gaps and uncertainty are explicit and actionable.

### Stage 7 - Define evaluations, impacts and risks

**Objective:** Specify proof before implementation.

**Coverage:** Normal journeys, supplied evaluation patients, identity conflicts, consent states, open deviations, idempotency conflicts, temporal contradictions, telemetry quality, outages, recovery, prompt injection, authority spoofing, PHI leakage, tool misuse, human override, latency, cost and performance.

**Artifacts:** Evaluation strategy, golden set, scenario catalogue, acceptance thresholds, AI impact assessment, harms/risk registers, risk treatments, oversight requirements and residual-risk template.

**Exit:** Every P0 requirement has a verification method and acceptance threshold.

### Stage 8 - Generate, test and select options

**Objective:** Select the simplest safe solution.

**Options:** Legacy patch, rules-only orchestrator, deterministic orchestrator plus one bounded assistant, multi-agent design, and buy/partner alternatives.

**Artifacts:** Solution catalogue, technical spikes, reference comparison, provider/model comparison, build-buy-partner analysis, TCO, trade-off matrix, preliminary ADRs and selected solution.

**Expected baseline:** Deterministic orchestrator plus one recommendation-only exception assistant; multi-agent behavior only if evaluation proves its value.

**Exit G2:** Approved solution with explicit trade-offs.

## Phase 3 - Design and specify

### Stage 9 - Design information architecture

**Artifacts:** Canonical data architecture, patient/batch/shipment/slot/deviation/event contracts, identity-resolution model, event envelope, schema-versioning rules, semantic model, metadata/provenance design, retrieval architecture, retention/disposition rules and data ADRs.

**Exit:** Information contracts are precise and testable.

### Stage 10 - Design AI and application architecture

**Target components:** API gateway, orchestration service, persistent state/event store, deterministic state machine, identity resolver, slot service, MES/QMS/logistics adapters, human-review queue, bounded exception assistant, audit service, UI, telemetry and evaluation pipeline.

**Artifacts:** C4 Context/Container/Component views, AI/RAG architecture, model-routing design, API/event contracts, prompt/context design, deployment topology, failure modes, AI-disabled mode and architecture ADRs.

**Exit:** Complete base architecture with explicit failure behavior.

### Stage 11 - Design agentic and multi-agent orchestration

**Objective:** Define bounded agency and human control.

**Artifacts:** Agent-suitability assessment, single-vs-multi-agent ADR, responsibility map, topology and sequence diagrams, state model, tool/action catalogue, identity/permission matrix, memory design, handoff protocol, termination/loop controls and approval/override/escalation matrix.

**Default authority:** AI may read, summarize and recommend. Authenticated humans authorize identity resolution, deviation closure, rerouting execution and QA release.

**Exit:** No agent has unbounded or hidden authority.

### Stage 12 - Design security, guardrails and supplier controls

**Artifacts:** Threat model, agent attack-surface map, trust boundaries, abuse cases, OWASP GenAI/Agentic mapping, Zero Trust controls, DLP/privacy architecture, human-factors assessment, automation-bias controls, supplier/model assessment, model/system cards, component register, SBOM/AIBOM and exit plan.

**Exit:** Controls cover input, context, model, tool, identity, output, audit and supplier risks.

### Stage 13 - Approve ADRs and delivery specification

**Artifacts:** Final ADR register, approved C4 baseline, PRD, functional requirements, NFRs, assurance requirements, acceptance criteria, API/data/event contracts, agent specifications, evaluation cases, telemetry/logging specification, SLO/SLA/error budgets, rollback requirements, traceability matrix and engineering backlog.

**Exit G3:** No implementation item lacks an ID, acceptance criterion, owner and verification method.

## Phase 4 - Engineer and assure

### Stage 14 - Engineer

Build three integrated vertical POCs on one shared platform.

#### POC 1 - Patient and identity readiness

Identity conflict detection, consent and authorization, site qualification, Chain of Identity linkage, safe state transitions and authorized human resolution.

#### POC 2 - Manufacturing disruption and slot orchestration

Persistent idempotent reservation, same-key/different-payload conflict, capacity constraints, logistics disruption, alternative recommendations, authenticated approval, audit and rollback.

#### POC 3 - Product, QA and thermal-release support

Manufacturing completion, QC, QMS status, deviations, controlled thermal evidence, Quality review, electronic approval and prevention of premature progression.

#### Shared engineering deliverables

Source, migrations, immutable fixtures, APIs, adapters, event store, state machine, audit trail, authorization policy, agent/prompt configuration, UI, Docker environment, CI, IaC where applicable, unit/contract/integration/property/end-to-end tests and as-built C4 views.

**Exit:** A clean clone reproduces all three workflows through shared services.

### Stage 15 - Evaluate, attack and internally assure

**Tests:** Supplied cases and failure injections, state/property tests, API contracts, concurrency/idempotency, lineage/provenance, task completion, grounding, prompt injection, authority spoofing, PHI leakage, tool misuse, malformed output, model/provider outage, loop/termination, recovery/replay, performance, latency, cost and human factors.

**Artifacts:** Evaluation harness, golden datasets, results, red-team findings, guardrail evidence, assurance report and residual-risk acceptance.

**Truth rule:** Codex can prepare internal assurance. Formal independent assurance remains pending until performed by a separate authorized reviewer.

**Exit G4:** All P0 tests pass and no critical unresolved risk remains.

### Stage 16 - Prepare operations, recovery and regulatory evidence

**Artifacts:** Operational RACI, SLO dashboard, agent/model/tool telemetry, alerts, runbooks, incident/rollback plans, AI-disabled mode, backup/recovery plan, RTO/RPO, chaos-drill evidence, SOPs/training, AI-system record, technical documentation, transparency records and regulatory evidence index.

**Exit G5:** Operationally ready for a controlled pilot, not declared production-ready.

## Phase 5 - Demonstrate, monitor and decide

### Stage 17 - Deploy progressively and integrate adoption

**Sequence:** Local reproducibility -> CI -> shadow demonstration -> controlled canary simulation -> pilot recommendation.

**Artifacts:** Release manifest, deployment record, shadow comparison, canary results, rollback decision, adoption dashboard, override/workaround logs, user feedback and updated SOPs.

**Exit:** Controlled service and adoption evidence exist.

### Stage 18 - Monitor and validate operational resilience

**Monitor:** Availability, latency, state failures, idempotency conflicts, source drift, provenance gaps, agent fallback, recommendation acceptance/rejection, overrides, PHI events, injections, model/prompt versions, token usage, cost per successful outcome, drift, loop alerts and recovery performance.

**Artifacts:** Dashboards, traces, continuous-eval results, drift reports, cost/availability reports, incidents, chaos/recovery results and updated runbooks.

**Exit:** Operational performance, risk and resilience are evidenced.

### Stage 19 - Prove value and tell the decision story

**Artifacts:** Measured before/after KPIs, benefits-realisation report, TCO and cost-to-value analysis, counter-metrics, waste reduction, unintended effects, executive SCQA paper, executive C4 view, demo script and decision recommendation.

**Exit:** Every benefit claim is measured or clearly labelled as a hypothesis.

### Stage 20 - Evaluate AIMS and decide lifecycle state

**Artifacts:** AIMS performance report, internal-audit findings, CAPA register, management-review package, control plan, updated risks/ADRs/evaluations and lifecycle recommendation.

**Expected capstone decision:** POC complete; controlled pilot recommended subject to external integration, validated electronic signatures, formal regulatory review and independent assurance.

**Exit G6:** Authorized scale/change/restrict/suspend/retire recommendation.

### Stage 21 - Retire and capture reusable IP

**Scope:** Close the capstone environment; do not claim retirement of the real enterprise estate.

**Artifacts:** Retirement plan, notifications, credential revocation, data/model/memory disposition, supplier closure, archived evidence pack, lessons learned, reusable ADR/C4/state-machine templates, evaluation harness, guardrail templates and reference architecture.

**Exit:** Capstone formally closed and reusable IP captured.

## Capabilities added explicitly

The operating model is supplemented with capabilities identified by the framework as not explicit:

- User journey and service design.
- Privacy-by-Design.
- Human factors and automation-bias assessment.
- Legal, contractual, licensing and IP assessment.
- Token efficiency and token economics.
- SLO/SLA/error-budget engineering.
- AI FinOps and cost per successful outcome.
- 30/60/90-day transformation roadmap.

## Working sequence

| Period | Stages | Outcome |
|---|---:|---|
| Week 1 | 1-4 | Approved mandate, evidence baseline, problem and use case |
| Week 2 | 5-8 | Domain/data readiness, evaluation plan and selected solution |
| Week 3 | 9-13 | Approved architecture and build-ready specification |
| Weeks 4-5 | 14 | Three integrated vertical POCs |
| Week 6 | 15-16 | Internal assurance, operations and recovery evidence |
| Week 7 | 17-18 | Controlled deployment simulation and resilience evidence |
| Week 8 | 19-21 | Value story, lifecycle decision, closeout and reusable IP |

## Final definition of done

The capstone is complete only when:

- The original evidence remains unchanged.
- Findings are reproducible.
- One canonical domain/state model exists.
- Requirements, ADRs, code, tests, evidence and KPIs are traceable.
- Three workflows use shared services and one consistent working dataset.
- Consequential actions require authenticated human authority.
- Safety gates fail closed.
- Supplied evaluation and failure cases execute.
- All P0 tests pass.
- Residual risks are visible.
- A clean clone runs without manual code changes.
- Reports separate facts from assumptions and targets.
- Operations and recovery evidence exist.
- The lifecycle recommendation is honest and defensible.
