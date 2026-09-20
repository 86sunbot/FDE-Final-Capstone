# Product Requirements Document - CGT Patient-to-Batch Control Tower

**Status:** Draft for Capstone Owner review; not clinical, Quality, regulatory, or production approval
**Product increment:** Synthetic local academic demonstration
**Source of client ask:** `source_baseline/participant/CHALLENGE_BRIEF.md`
**Engineering specification:** `01_BUILD_READY_SPECIFICATION.md` and `requirements/requirements.csv`

## 1. Client problem and product outcome

An autologous Cell and Gene Therapy journey has one patient-specific collection, shipment, manufacturing batch, Quality decision, return shipment, and eventual treatment milestone. The inherited synthetic estate spreads those facts across systems and shadow work. An operator cannot safely answer: *Which identity and material are these records about? What is known now, from which source, under which policy, and who may decide what happens next?*

The product outcome is a governed, evidence-bearing operational view and three workflow proofs. The app must make conflicts, missing evidence, temporal anomalies, authority, and recovery visible. It must not convert a model answer, MES completion, ERP availability, or a single sensor reading into Quality release.

## 2. Intended users and jobs

| User role | Job in this increment | Consequential authority |
|---|---|---|
| Coordinator | Inspect a patient journey, identify blockers, open and own an exception | No identity merge or product release |
| Planner | Inspect slot state, submit an authorized simulated reservation, reconcile unknown outcomes | Simulated slot command only |
| Identity Authority | Review an evidence-bound identity proposal | Simulated identity decision only |
| Quality Authority | Inspect QC, deviation, thermal, and QMS evidence packet | Simulated release decision only |
| Viewer/executive | Understand current state, provenance, limitations, and next gate | Read only |
| Optional assistant | Produce a cited, uncertain summary of deterministic context | None; no mutating tool |

These roles are synthetic test roles. Real organizational identities, signatures, and qualifications are not supplied.

## 3. Scope and workflows

### W1 - Patient identity and milestone readiness

The user sees CRM and clinical assertions separately, including disagreements. A conflict opens an owned case. A candidate relationship is a proposal, not a fact, until an authorized decision binds exact evidence and payload. Readiness checks identity, consent, financial authorization, and site controls for a named milestone; missing or contradictory facts are `UNKNOWN` and do not progress the journey.

**Acceptance:** no silent identity link; material facts cite evidence; unauthorized or stale approval is denied; withdrawn consent blocks downstream continuation. Traces: `REQ-ID-001/002`, `REQ-GATE-001`, `REQ-FDN-002/004`, `REQ-AUTH-001`.

### W2 - Manufacturing slot and disruption preview

The planner sees scheduler and MES state separately. A reservation has a payload-bound idempotency key. A timeout after possible success is `OUTCOME_UNKNOWN`, requires query/reconciliation, and cannot be blindly retried. Partial effects require explicit compensation. A source-backed disruption preview lists affected milestones, evidence, owner, uncertainty, and candidate re-planning questions; it does not autonomously change capacity or clinical plans.

**Acceptance:** one effect under replay/concurrency; changed-payload conflict; unknown-outcome reconciliation before retry; apheresis delay and suite/courier outage previews show downstream dependencies rather than only opening a generic case. Traces: `REQ-CMD-001/002/003`, `REQ-CASE-001`, `REQ-FDN-003`, `REQ-INJ-001`.

### W3 - Quality evidence and release support

The user sees MES, LIMS/QC, deviations, thermal observations, and QMS assertions with their source and state. Manufacturing completion is not release. QC disposition, blocking deviation status, sensor quality, and authorized Quality approval are explicit prerequisites. Missing or ambiguous evidence yields `UNKNOWN` or a blocker; the app cannot silently apply superseded SOP logic.

**Acceptance:** MES/ERP/model output never creates `ProductReleased`; only scoped Quality Authority can approve a complete synthetic packet; QMS outage preserves Quality authority and safe degraded mode. Traces: `REQ-QUAL-001/002`, `REQ-AUTH-001/002`, `REQ-AI-001/003`.

## 4. Screens and demo contract

1. **Scope/status:** synthetic-only, AI mode, three workflow proofs, internal-test scope, production prohibition, open CAPAs.
2. **Source-case explorer:** choose supplied `EVAL-001` through `EVAL-006`; display original patient key, source rows, source-system disagreements, evidence locators, occurrence-time source journey order, unresolved authority/lineage/release gates, and an explicitly non-authoritative interpretation. Traces: `REQ-SRC-001/002/003`.
3. **Three-POC run:** execute the shared services, show before/after states, evidence references, command replay and audit result. A scripted fixture is labelled as such, not passed off as a v2 source migration.
4. **Disruption preview:** choose supplied `INJ-001` through `INJ-010`; show trigger, affected domains, dependency cascade/unknowns, owner, and prohibited automatic actions. A preview is not a committed schedule or disposition. Trace: `REQ-INJ-001`.
5. **Limits and decision:** show that human studies, live-model value, enterprise integration, real KPI improvement, independent assurance, and production readiness remain unproven.

The existing browser Control Tower and FastAPI are demo surfaces, not production identity or regulated record systems.

## 5. Functional, non-functional, and assurance requirements

The canonical requirements are in `requirements/requirements.csv`; the verification result is in `requirements/verification_matrix.csv`. In addition to W1-W3, this increment requires read-only access to the frozen v2 source fixtures, typed IDs and units, occurred/recorded time separation, source locators, server-side role/scope checks, tamper detection, an AI-off path, and repeatable local setup.

The originally proposed 20-concurrent-client latency condition in Stage 7 is not met by the existing micro-benchmark. The open protocol is in Stage 15 `08_REGISTERED_JOURNEY_LOAD_TEST_PROTOCOL.md`. Load evidence must either be executed under the registered conditions or remain `NOT_VERIFIED`. No local result is extrapolated to global scale.

## 6. Out of scope and kill criteria

Out of scope: real patient records; clinical advice; automatic COI/COC adjudication; actual reservation with MES; Quality product disposition; validated electronic signature; real infusion decision; live supplier/model integration; globally scalable production infrastructure.

Stop or disable a path if an unauthorized consequential action is accepted, a source conflict is silently flattened, an ambiguous external effect is blindly retried, a model answer changes canonical state, a release is inferred from MES/ERP, or a P0 exception lacks an owner. Invalid AI output must disable only AI, not deterministic service.

## 7. Measurement and decision

North star: safe, on-time, evidence-complete individualized journeys with accountable human authority. POC measures are safety-gate violations, invented links, duplicate effects, source/time provenance, owned exceptions, original-case coverage, latency, and operator evidence inspection. The supplied business KPI baselines are challenge inputs, not reproduced before/after outcomes; see Stage 3 and Stage 19.

The academic exit gate requires an exact PRD-to-requirement-to-code-to-test-to-demo map, execution of the original v2 evaluation seeds and disruption injects at the claimed coverage level, no P0 internal test failure, and explicit open external evidence. A real pilot needs accountable policy, IAM/signature, regulatory/privacy, integration, human-factor, and independent-assurance decisions outside this PRD.

## 8. Handoff and approval

| Handoff | Canonical location |
|---|---|
| Client mandate and ten deliverables | `source_baseline/participant/CHALLENGE_BRIEF.md` |
| Product requirements and user workflows | This PRD |
| Engineering requirements and tests | `requirements/requirements.csv`; `requirements/verification_matrix.csv` |
| Domain model and authority | `docs/stages/stage_05`; `docs/stages/stage_04` |
| Architecture, contracts, migration | `docs/stages/stage_09`; `docs/stages/stage_10`; `08_BROWNFIELD_MIGRATION_STRATEGY.md` |
| Code, app, and as-built evidence | `src/fde_capstone`; `tests`; `docs/stages/stage_14` |
| TEVV and lifecycle decision | `docs/stages/stage_15`; `docs/stages/stage_20` |

**Capstone Owner review:** Pending. Codex may implement and internally verify this synthetic increment, but cannot sign for Clinical, Quality, Legal, Privacy, Security, or independent assurance.
