# CGT Capstone - Implementation Sequence

**Programme state:** ACADEMIC CAPSTONE COMPLETE; lifecycle decision RESTRICT AND CHANGE  
**Operating model:** 21-stage AI FDE model  
**Delivery loop:** `SPECIFY -> BUILD -> VERIFY -> SHIP -> REPEAT`  
**Source rule:** The original ZIP remains immutable; all implementation uses verified copies.

## How the sequence works

The 21 stages are executed in six gated waves. Work may be prepared ahead, but no wave is represented as approved until its accountable human owner accepts the gate evidence. Every material requirement maintains this chain:

`Evidence -> Lens/root cause -> Requirement -> ADR -> Code -> Test/eval -> KPI -> Decision`

## Wave 1 - Establish the evidence and problem

### Step 1: Establish mandate and controls - Stage 1

- Freeze and checksum the original challenge package.
- Define scope, outcomes, exclusions and evidence-handling rules.
- Identify users, affected groups, owners and consequential decision authorities.
- Record assumptions and decisions that require human confirmation.

**Current state:** APPROVED for academic POC; production stakeholder validation remains pending.

### Step 2: Reproduce the brownfield estate - Stage 2

- Extract a read-only verified baseline.
- Inventory files, datasets, code, contracts and controls.
- Run existing tests and reproduce defects from source evidence.
- Map the journey, systems, data flows, trust boundaries, waste and eight legacy lenses.
- Decide what to reuse, replace or retire from the inherited prototype.

**Current state:** APPROVED for academic POC; production stakeholder validation remains pending.

### Step 3: Frame the measurable problem - Stage 3

- Write the SCQA and prioritized problem statement.
- Separate symptoms from root causes.
- Establish supplied and independently reproduced KPI baselines.
- Define CTQs, value hypotheses, counter-metrics, success criteria and kill criteria.

**Current state:** APPROVED for academic POC.

### Step 4: Bound regulation and AI use - Stage 4

- Define intended purpose and deployment context.
- Screen 21 CFR Part 11, EU AI Act, ISO 42001/42005, privacy, records, licensing and IP relevance.
- Identify prohibited uses and decisions that must remain human-authorized.
- Compare manual, rules-only and AI-assisted variants.
- Produce three use-case cards and a value-risk-feasibility decision.

**Current state:** APPROVED for academic POC under `stage_04/07_G1_DECISION_RECORD.md`.

**Gate G1:** Approve the problem, use cases and deterministic/AI boundary.

## Wave 2 - Model, qualify and select

### Step 5: Model the business - Stage 5

- Define the shared glossary and bounded contexts.
- Model patient, identity, collection, shipment, slot, batch, QC, deviation, release and infusion relationships.
- Specify versioned decision tables, events and legal state transitions.
- Make unknown/missing safety evidence fail closed.

**Current state:** READY FOR REVIEW; domain-owner validation remains a production gap.

### Step 6: Qualify data and knowledge - Stage 6

- Profile quality, lineage, temporal behavior, provenance and permissible use.
- Define attribute-level authority instead of one global source of truth.
- Catalogue SOP versions, knowledge gaps and representativeness limits.
- Reconstruct KPI formulas where the evidence permits; preserve unresolved formulas as gaps.

**Current state:** READY FOR REVIEW; accountable data/Privacy/Quality review remains a production gap.

### Step 7: Define proof before code - Stage 7

- Turn the six supplied evaluation cases and ten failure scenarios into executable specifications.
- Add normal, boundary, adversarial, privacy, authorization, outage and recovery cases.
- Define acceptance thresholds and P0/P1 severity.
- Complete impact, harms, threat and risk-treatment registers.

**Current state:** READY FOR REVIEW; 57 cases are specified and explicitly not run.

### Step 8: Compare solution options - Stage 8

- Spike legacy patch, rules-only orchestration and deterministic-plus-bounded-AI designs.
- Compare safety, value, complexity, lock-in, operability and cost.
- Select the simplest option that meets the tests.
- Default to deterministic orchestration plus one recommendation-only assistant unless evidence supports more agency.

**Current state:** APPROVED; O3 selected under delegated academic authority, with O2 mandatory as AI-off fallback.

**Gate G2:** Approve the selected solution and trade-offs.

## Wave 3 - Design a build-ready system

### Step 9: Design information contracts - Stage 9

- Specify typed data and event envelopes with occurred/recorded time and provenance.
- Define identity assertions, canonical views, versioning, retention and evidence links.
- Create contracts for patients, collections, shipments, slots, batches, QC, deviations and decisions.

### Step 10: Design application and AI architecture - Stage 10

- Create C4 context, container and component views.
- Define APIs, persistent state/event stores, adapters, review queue, audit service, UI and telemetry.
- Specify AI context, structured output, grounding, failure modes and AI-disabled operation.

### Step 11: Bound agent orchestration - Stage 11

- Decide whether one assistant is sufficient; add multiple agents only with measured justification.
- Define read/recommend tools separately from mutating tools.
- Specify authenticated approvals, handoffs, termination, escalation and memory boundaries.

### Step 12: Engineer security and supplier controls - Stage 12

- Threat-model identity, input, retrieval, model, tool, output and supply chain.
- Define Zero Trust authorization, DLP, PHI controls, audit, guardrails and provider fallback.
- Produce supplier records, model/system cards, SBOM/AIBOM and exit plan.

### Step 13: Freeze the delivery specification - Stage 13

- Approve ADRs, requirements, NFRs, contracts, eval cases, telemetry and rollback behavior.
- Map each backlog item to an ID, owner, acceptance criterion and test.
- Verify complete requirements-to-evidence traceability.

**Gate G3:** Approve the build-ready specification.

## Wave 4 - Build in safe vertical increments

### Step 14A: Build the shared deterministic foundation

- Repository structure, migrations, immutable fixtures and working database.
- Typed identifiers/units, bitemporal events and canonical state machine.
- Authentication/authorization policy, audit ledger, inbox/outbox, command ledger and idempotency.
- Adapter interfaces, case lifecycle, observability and AI-disabled mode.
- CI with unit, contract and migration tests.

### Step 14B: POC 1 - Patient and identity readiness

- Detect identity conflicts without inventing links.
- Evaluate consent, authorization and site prerequisites by milestone.
- Build an evidence-bearing readiness view and human resolution case.
- Test safe abstention, authority, corrections and replay.

### Step 14C: POC 2 - Manufacturing disruption and slot orchestration

- Implement persistent payload-bound idempotent reservations.
- Model capacity, partial transactions, retry, conflict and compensation.
- Recommend alternatives without executing them.
- Require authenticated human approval for rerouting or reservation changes.

### Step 14D: POC 3 - Product, QA and thermal-release support

- Separate manufacturing completion, QC, QMS release and journey readiness.
- Model deviations, evidence links, assay disposition and controlled thermal evidence.
- Assemble the review packet and blocker explanation.
- Reserve product disposition/release for an authorized Quality role.

### Step 14E: Integrate and demonstrate

- Run all POCs through the same APIs, domain rules, event store, audit and UI.
- Add end-to-end journeys and failure recovery.
- Produce Docker/local run commands, CI evidence and as-built C4 diagrams.

## Wave 5 - Verify and prepare controlled operation

### Step 15: TEVV and attack - Stage 15

- Execute all golden, failure, property, concurrency, authorization and recovery tests.
- Test prompt injection, authority spoofing, PHI leakage, tool misuse, malformed output and model outage.
- Measure task success, grounding, latency, cost and human override.
- Fix defects and rerun; publish residual risk honestly.

**Gate G4:** All P0 tests pass; no unresolved critical risk.

### Step 16: Prepare operations - Stage 16

- Define SLOs, dashboards, alerts, runbooks and incident/rollback procedures.
- Test backup, restore, RTO/RPO, degraded mode and chaos scenarios.
- Prepare SOP, training, technical and regulatory evidence indexes.

**Gate G5:** Approve readiness for a controlled simulated pilot.

## Wave 6 - Demonstrate, measure and decide

### Step 17: Deploy progressively - Stage 17

- Demonstrate local reproduction, CI, shadow comparison and canary simulation.
- Capture release manifests, rollback evidence, overrides, workarounds and user feedback.
- Do not claim real production deployment without evidence.

### Step 18: Monitor resilience - Stage 18

- Monitor service, state, source drift, provenance, authority, model fallback, cost and safety counter-metrics.
- Run incident and recovery exercises and update runbooks.

### Step 19: Prove value - Stage 19

- Compare before/after KPIs with explicit populations and formulas.
- Separate deterministic benefit from the incremental AI benefit.
- Report counter-metrics, TCO, limitations and unintended effects.

### Step 20: Make the lifecycle decision - Stage 20

- Compile assurance, internal audit, CAPA, control and management-review evidence.
- Recommend scale, change, restrict, suspend or retire based only on results.

**Gate G6:** Authorized lifecycle decision.

### Step 21: Close the capstone and capture reusable IP - Stage 21

- Retire the capstone environment safely; do not claim retirement of the real enterprise estate.
- Archive evidence and dispose of credentials/data/model memory as specified.
- Capture reusable ADR, C4, state-machine, guardrail and evaluation templates.

## Final execution result

All 21 stages were executed in `FDE-Final-Capstone`. Stages 9–13 produced build-ready contracts and controls; Stage 14 produced one shared foundation, a browser Control Tower and three integrated POCs; Stage 15 recorded 77 automated passes and 55 structural catalog passes with two external human-study cases inconclusive; Stages 16–19 completed local recovery, release, monitoring and value simulations; Stages 20–21 recorded the restrict/change decision, seven open CAPAs, retirement and reusable IP.

No immediate engineering work remains for the academic deliverable. Any real pilot begins a new controlled programme by addressing the seven CAPAs in `stage_20/02_INTERNAL_AUDIT_AND_CAPA.md`.

## Progress-control rules

- `READY FOR REVIEW` means artifacts exist and Codex checks pass; it does not mean human approval.
- `APPROVED` requires a named accountable decision and a recorded date/evidence link.
- Failed acceptance criteria move the item to `REWORK`; they are not softened after implementation.
- Every work session updates `CAPSTONE_PROGRESS_TRACKER.md` with tests, risks, decisions and the next executable action.
- Every stage review lists facts, assumptions, gaps and the human decisions still required.
