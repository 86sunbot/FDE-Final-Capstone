# Stage 4 - AI Suitability and Non-AI Alternative

**Status:** Option-screen hypothesis; Stage 8 must validate with spikes and evaluation  
**Last updated:** 2026-09-14

## 1. Decision question

Does AI add measured value after the domain, evidence, workflow and authority controls are implemented, or can deterministic engineering solve the need more safely and cheaply?

## 2. Task-level suitability

| Task | Variability/ambiguity | Consequence if wrong | Deterministic feasibility | AI suitability | Decision |
|---|---|---:|---:|---:|---|
| Validate state transition | Low | Critical | High | None | Deterministic only |
| Enforce consent/site/authorization/Quality gate | Low once policy is specified | Critical | High | None | Deterministic only |
| Check command idempotency and payload conflict | Low | High | High | None | Deterministic only |
| Calculate typed temporal/thermal features | Low-to-medium | High | High with controlled specification | None for decision | Deterministic only |
| Authenticate/authorize/sign | Low | Critical | High | None | Deterministic only |
| Resolve identity/COI | High | Critical | Partial | Unsafe as autonomous AI | Human decision supported by deterministic evidence; optional summary |
| Extract candidate facts from messy notes/email | High | Medium-to-high | Low-to-medium | Potentially useful | AI-assisted with untrusted-content isolation and verification |
| Summarize cross-system evidence | Medium/high volume | Medium/high | Possible but rigid | Potentially useful | AI-assisted, cited and reviewable |
| Explain blockers and downstream impact | Medium | Medium/high | Core causal graph deterministic; language variable | Potentially useful | Deterministic facts plus AI explanation |
| Enumerate feasible slot alternatives | Low/structured | High | High | None | Deterministic constraint engine |
| Rank feasible alternatives with qualitative context | Medium | High | Partial | Conditional | AI-assisted only after deterministic filtering; human chooses |
| Close deviation/disposition/release | High | Critical | Human procedure | Prohibited | Human-authorized only |

## 3. Rules-only reference solution

The non-AI solution contains:

1. Source adapters that preserve source-specific evidence.
2. A canonical domain/event model and bitemporal projection.
3. Deterministic identity conflict detection with a human resolution queue.
4. Versioned decision tables for readiness and legal state transitions.
5. A constraint engine for feasible slot alternatives.
6. A persistent inbox/outbox, command ledger, idempotency and compensation workflow.
7. A case-management UI with filters, evidence links, ownership, SLA and escalation.
8. Quality evidence packets generated from structured templates.
9. Authentication, authorization, approval/signature records and immutable audit.
10. Telemetry, replay, backup/recovery and operational runbooks.

This solution is the safety baseline and must remain usable when AI is disabled.

## 4. AI-assisted variant

The AI variant adds only:

- candidate extraction from unstructured notes/messages;
- evidence-grounded summaries;
- plain-language blocker and impact explanations; and
- ranking/explanation of alternatives already proven feasible by deterministic code.

The AI cannot write directly to clinical, identity, MES, QMS, logistics or release state. A recommendation has no business effect until an authenticated human decides and deterministic policy validates execution.

## 5. Comparative evaluation design

Use a three-arm evaluation:

| Arm | Capability | Purpose |
|---|---|---|
| A - Existing/manual | Supplied formal and shadow workflows | Establish task/error/traceability baseline where measurable |
| B - Rules-only | Full deterministic orchestration and case UI | Measure value attributable to domain/workflow engineering |
| C - Rules plus bounded AI | Arm B plus optional assistant | Measure incremental AI value and harm |

Measure the same cases and operator tasks across arms:

- task completion and time;
- evidence/provenance completeness;
- identity and state correctness;
- unauthorized or unsafe action;
- false block/false clear;
- recommendation acceptance, rejection and correction;
- automation bias and evidence inspection behavior;
- latency, availability and recovery;
- prompt-injection/PHI/DLP failures; and
- cost per correctly resolved case.

AI is selected only if Arm C delivers a meaningful improvement over Arm B without breaching any P0 threshold or worsening counter-metrics beyond the approved limit.

## 6. AI-specific go/no-go conditions

Proceed to an AI-assisted POC only if:

- the deterministic evidence and workflow foundation is complete;
- the task involves enough unstructured ambiguity/volume to justify AI;
- trusted evidence can be cited in the output;
- incorrect output is detectable and safely reviewable;
- an accountable human has time, skill and authority to review it;
- the system can abstain and fall back to the rules-only view;
- provider/data-use/privacy controls are acceptable; and
- an evaluation can measure incremental value and harm.

Do not proceed, or remove AI, if:

- the output becomes a release, disposition, clinical or identity decision;
- users cannot realistically verify the evidence;
- prompts/context require uncontrolled PHI disclosure;
- the model can invoke consequential mutations;
- AI-disabled operation is unsafe or unusable;
- P0 grounding, authority, security or privacy tests fail; or
- cost/latency/rejection outweighs measured benefit.

## 7. Preliminary recommendation

Build the rules-only platform as the product. Treat the bounded assistant as a replaceable, optional feature behind an adapter and feature flag. Stage 8 must compare the two variants; Stage 15 must attack the selected behavior; Stage 19 must separate deterministic value from AI increment.
