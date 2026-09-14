# Stage 4 - Use-Case Cards and AI Boundaries

**Status:** Proposed for G1 review  
**Last updated:** 2026-09-14

## Boundary legend

- **Deterministic:** typed rules, constraints, state transitions, calculations or data retrieval with reproducible output.
- **AI-assisted:** non-authoritative extraction, summarization, explanation or option ranking; output may be wrong and requires evidence-aware review.
- **Human-authorized:** consequential judgment or action attributable to an authenticated accountable person.
- **Prohibited:** capability the capstone must not permit an AI/agent to perform.

## UC-01 - Patient and identity readiness

| Field | Definition |
|---|---|
| Primary users | Clinical Operations coordinator; identity/data steward; treatment-site coordinator |
| Job to be done | Understand whether the correct patient/material journey has sufficient evidence to proceed to a specified milestone and resolve conflicts safely |
| Trigger | New/changed patient, identity, consent, authorization, site, collection or COI evidence |
| Inputs | Source-specific identity assertions, patient records, consent, authorization, site qualification, collections, events and policy versions |
| Deterministic output | Evidence-completeness and conflict result; milestone prerequisites; allowed/blocked/unknown state; cited blockers |
| AI-assisted output | Plain-English conflict/evidence summary and suggested investigation order |
| Human authority | Resolve identity assertion; approve exceptional reconciliation; confirm consequential COI correction under procedure |
| Prohibited AI action | Merge patient identities, establish lineage, suppress conflicting evidence, approve a gate or alter source records |
| Value hypothesis | Reduce evidence-search and reconciliation effort while preventing false readiness |
| Principal harms | Wrong-patient linkage, concealed uncertainty, PHI overexposure, automation bias and treatment delay from false blocks |
| Minimum evidence | All assertions with source, observed/effective time, conflicts, matching features, confidence/quality and rule version |
| Success condition | Correct link or explicit abstention; zero invented links; no P0 gate bypass; full provenance |
| Kill condition | Any autonomous identity resolution or missing evidence treated as safe |

### UC-01 decision decomposition

1. Retrieve evidence - deterministic.
2. Normalize without destroying raw/source values - deterministic.
3. Detect conflicts and calculate rule prerequisites - deterministic.
4. Summarize evidence - optional AI-assisted.
5. Decide identity resolution/COI correction - human-authorized.
6. Apply approved resolution through audited workflow - deterministic execution after authorization.

## UC-02 - Manufacturing disruption and slot orchestration

| Field | Definition |
|---|---|
| Primary users | Manufacturing planner; supply-chain coordinator; logistics coordinator |
| Job to be done | Recover safely from capacity/logistics disruption without duplicate or contradictory reservations |
| Trigger | Slot change, site outage, capacity conflict, logistics delay, retry or cross-system disagreement |
| Inputs | Current slot/MES state, capacity, journey priority policy, logistics feasibility, dependencies, command history and idempotency key |
| Deterministic output | Constraint violations, feasible alternatives, command state, payload-bound idempotency result and compensation requirement |
| AI-assisted output | Evidence-grounded impact summary and ranked feasible alternatives with stated trade-offs |
| Human authority | Select/approve a reroute, exception override or consequential reservation change |
| Prohibited AI action | Reserve/cancel/reroute autonomously, change priority policy, override capacity/safety constraint or hide a partial failure |
| Value hypothesis | Reduce conflict/recovery time and manual coordination while eliminating duplicate effects |
| Principal harms | Lost capacity, wrong prioritization, patient delay, repeated action and irrecoverable partial transaction |
| Minimum evidence | Current source states, capacity snapshot, constraint/rule versions, alternatives, affected journeys, command ledger and actor identity |
| Success condition | Same-key replay produces no extra side effect; different payload conflicts; failure reaches a known recoverable state |
| Kill condition | Duplicate side effect, unowned compensation or autonomous consequential change |

### UC-02 decision decomposition

1. Reconcile source state and command history - deterministic.
2. Validate constraints and enumerate feasible alternatives - deterministic.
3. Explain impact/rank already-feasible options - optional AI-assisted.
4. Choose consequential action - human-authorized unless a separately approved low-risk deterministic policy exists.
5. Execute through outbox/adapter and observe result - deterministic.
6. Compensate/escalate partial failure - deterministic workflow plus human exception authority.

## UC-03 - Product, QA and thermal-release support

| Field | Definition |
|---|---|
| Primary users | Quality reviewer/QP; manufacturing operations; logistics quality specialist |
| Job to be done | Assemble and understand product evidence without confusing manufacturing completion with authorized Quality release |
| Trigger | Manufacturing completion, QC result, deviation, thermal alert, shipment arrival or QMS state change |
| Inputs | Batch/MES state, QC results and disposition, QMS status, deviations and evidence links, raw thermal profile and quality, shipper evidence, SOP version and shipment events |
| Deterministic output | Evidence packet completeness, unresolved blockers/unknowns, valid transitions and Quality-authority requirement |
| AI-assisted output | Review-packet summary, evidence contradictions, questions for investigation and non-binding explanation |
| Human authority | Determine deviation impact, thermal/product disposition, close deviation and approve product/batch release |
| Prohibited AI action | Infer disposition from incomplete data, close deviations, electronically sign, release product or authorize conditioning/infusion |
| Value hypothesis | Shorten evidence assembly/review preparation without weakening Quality authority or traceability |
| Principal harms | Premature progression, false release confidence, missed deviation/telemetry issue and fabricated citation |
| Minimum evidence | Raw and derived evidence, data quality, duration/profile calculation, relevant SOP/rule versions, deviations, QC disposition and authenticated approval |
| Success condition | Manufacturing/ERP status never substitutes for release; every summary cites evidence and exposes unknowns |
| Kill condition | Any path bypasses QMS/authorized Quality decision or presents AI recommendation as disposition |

### UC-03 decision decomposition

1. Retrieve and link evidence - deterministic with explicit unresolved links.
2. Evaluate completeness and controlled prerequisite rules - deterministic.
3. Calculate approved typed thermal features - deterministic; no invented threshold.
4. Summarize the evidence packet - optional AI-assisted.
5. Determine deviation/thermal/product disposition and release - human-authorized.
6. Record signature/decision and permit the next transition - controlled deterministic workflow.

## Shared AI output contract

Every AI-assisted output must include:

- use-case and recommendation ID;
- model, prompt/template and policy versions;
- evidence references with source and time;
- extracted facts separated from inference;
- conflicts, missing evidence and uncertainty;
- proposed options and trade-offs, if applicable;
- explicit statement of what the assistant cannot decide;
- required human authority and next safe action;
- content-safety/prompt-injection handling result; and
- immutable generation and reviewer audit records.

If this contract cannot be satisfied, the assistant must abstain and return the deterministic evidence view.

## Shared authority rule

Recommendation, approval and execution are three separate events. The human approver's authority is derived from authenticated identity and policy. It is never accepted from an API request field, prompt, email, document or model output.
