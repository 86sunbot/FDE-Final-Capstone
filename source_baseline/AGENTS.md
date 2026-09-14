# AGENTS.md — Instructions for coding agents

## Mission
Treat this repository as a brownfield enterprise system, not a greenfield rewrite. Preserve evidence, identify assumptions, and make changes in small, testable increments.

## Non-negotiables
- Do not treat any single database/table/API as the global source of truth without evidence.
- Do not "repair" synthetic inconsistencies globally unless a requirement explicitly calls for it; many are intentional challenge signals.
- Never fabricate a patient/material/batch linkage when identifiers conflict. Represent uncertainty and evidence.
- Do not make consequential clinical, quality-release, chain-of-identity or chain-of-custody decisions autonomous.
- Prefer reversible changes and explicit migration paths over big-bang replacement.
- Separate conventional deterministic engineering from AI-assisted/agentic components.
- Any AI-generated recommendation must expose supporting evidence, confidence/uncertainty, authority requirement and audit metadata.

## Engineering expectations
- Add tests before fixing an intentional defect.
- Keep patient/material/batch identity resolution explainable.
- Preserve raw events and provenance.
- Model event time separately from ingestion/recorded time.
- Treat units as typed data, not free text.
- Use idempotency for cross-system commands.
- Prefer explicit state machines over strings scattered in code.

## Local-first constraint
The baseline must remain runnable without cloud credentials. Optional LLM integrations must be adapters, disabled by default.
