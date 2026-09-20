# Stage 8 - Preliminary Architecture Decision Records

**Status:** PROPOSED; Stage 13 will make build-ready ADRs

## ADR-P01 - Clean solution tree

**Decision:** Build outside `source_baseline`; treat the supplied implementation as immutable comparison evidence.  
**Reason:** Core semantics require replacement and source integrity must remain provable.  
**Consequence:** Useful fixtures/contracts may be copied only with provenance and validation.

## ADR-P02 - Modular monolith first

**Decision:** One local deployable with explicit domain/application/port/adapter/UI boundaries.  
**Reason:** It minimizes distributed failure modes while preserving later extraction seams.  
**Consequence:** Module dependency rules and contract tests are mandatory.

## ADR-P03 - Evidence assertions and canonical projections

**Decision:** Preserve source assertions and derive evidence-bearing canonical views; do not create one mutable “golden patient” row.  
**Reason:** Source conflicts and bitemporal truth are first-class domain facts.  
**Consequence:** Display and decisions cite source, occurred/effective and recorded times.

## ADR-P04 - Durable command ledger and semantic idempotency

**Decision:** Persist a payload-bound command before dispatch and reconcile ambiguous outcomes before retry.  
**Reason:** Integration retries can duplicate high-impact external effects.  
**Consequence:** Idempotency conflicts, unknown outcomes and compensation are explicit states.

## ADR-P05 - Human authority as server-side policy

**Decision:** Consequential approval is a separate authenticated event enforced by server policy.  
**Reason:** UI labels, request payloads and model text are not authority.  
**Consequence:** Separation of duties and approval-payload integrity are testable.

## ADR-P06 - One optional bounded assistant

**Decision:** Add one read/recommend assistant behind a feature flag and provider-neutral port. It has no mutating/consequential tool.  
**Reason:** This permits AI value testing without making AI a workflow dependency.  
**Consequence:** Invalid/outage output falls back to deterministic mode; multi-agent is rejected unless later evidence justifies it.

## ADR-P07 - Local POC persistence and portability

**Decision:** Use a local transactional database for the capstone behind repository interfaces; production technology is undecided.  
**Reason:** The task requires reproducibility, not premature production infrastructure.  
**Consequence:** Migrations, constraints, backups and replay are still required; no production scalability claim follows.

## ADR-P08 - Evaluation and telemetry are product features

**Decision:** Every command, decision, model call and scenario result carries trace/correlation and evidence references.  
**Reason:** The capstone must prove behavior, not only demonstrate it.  
**Consequence:** Stage 9-13 contracts include evaluation and observability fields from the start.
