# Stage 8 - Solution Option Catalogue

**Status:** READY FOR G2 REVIEW

## Non-negotiable constraints

Every viable option must preserve evidence provenance, source-specific authority, explicit unknown states, typed identifiers, occurred/recorded time, semantic idempotency, human consequential authority, auditable decisions and useful operation with AI disabled. The original ZIP remains read-only evidence.

## Options

### O1 - Patch the inherited prototype

Keep the supplied FastAPI/repository structure and repair defects in place.

- Advantage: shortest route to a familiar-looking demo.
- Problem: direct database joins, naive readiness/release rules, weak idempotency and disconnected contracts would require changing the core semantics rather than applying a small patch.
- Decision: reject. Preserve it as comparison evidence only.

### O2 - Clean deterministic rules-only modular monolith

Build one deployable application with separated domain, application, adapter, persistence, authorization, audit and UI modules. Use versioned rules and evidence-bearing state projections.

- Advantage: simplest option with a credible safety and operability hypothesis.
- Limitation: does not test whether a bounded assistant reduces evidence-review effort.
- Decision: retain as the required base product and fallback.

### O3 - O2 plus one bounded optional assistant

Use exactly the O2 platform and add one provider-neutral assistant behind a feature flag. It may summarize cited evidence and recommend next actions; it has no consequential tool or authority event.

- Advantage: preserves the deterministic safety path while enabling B-versus-C evaluation of AI value and harm.
- Cost: additional schema, grounding, privacy, failure, human-factor and monitoring work.
- Decision: recommended for the academic capstone. If AI fails Stage 15 value/safety tests, ship/demonstrate O2 mode only.

### O4 - Agent-first multi-agent orchestration

Use specialized identity, scheduling, Quality and operations agents with inter-agent handoffs.

- Advantage: can demonstrate elaborate orchestration.
- Problem: expands authority, handoff, loop, debugging, evaluation and failure surfaces without evidence that the use case needs it.
- Decision: reject for this capstone.

### O5 - Buy or partner for a SaaS workflow platform

Configure a commercial workflow/AI product and integrations.

- Advantage: potential production capabilities and vendor support.
- Problem: no approved procurement requirements, supplier evidence, data-processing terms, regulated-use position, integration contracts or verified total cost are available.
- Decision: defer to a real production market scan; do not invent a vendor choice.

### O6 - Full distributed microservices rebuild

Create separate identity, journey, scheduling, Quality, command, AI and audit services.

- Advantage: independent scaling and organizational ownership potential.
- Problem: excessive distributed consistency, deployment and operational burden for a local capstone.
- Decision: reject for capstone scope; preserve clean internal boundaries so later extraction remains possible.

## Selected shape

O3 is a modular-monolith deployment of an O2 deterministic core plus one optional, recommendation-only assistant. “One deployable” does not mean “one unstructured codebase”: module and contract boundaries remain explicit and testable.
