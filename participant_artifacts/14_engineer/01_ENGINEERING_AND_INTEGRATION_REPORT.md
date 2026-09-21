# Stage 14 - Engineering and Integration Report

**Status:** IMPLEMENTED AND INTERNALLY VERIFIED  
**Scope:** Synthetic local academic POC

## Delivered foundation

- Python modular application under `src/fde_capstone`.
- Transactional SQLite schema for evidence, assertions, events, audit, cases, identity proposals/links, commands, simulated reservations, Quality evidence, recommendations and metrics.
- Server-side role/scope authorization and audited denials.
- Digest-addressed evidence, bitemporal assertions and evidence-required events.
- Tamper-evident audit hash chain.
- Owned exception lifecycle.
- Payload-bound semantic idempotency, unknown outcome, reconciliation and compensation.
- Quality evidence packet and authority-separated release.
- Provider-neutral assistant gateway; `off` by default; deterministic fake for tests only.
- Responsive browser Control Tower, CLI, FastAPI surface, Dockerfile, CI workflow, SBOM/AIBOM and release manifest.
- The Control Tower runs the same isolated three-POC orchestration path as the CLI, displays evidence/audit results and preserves the synthetic-only and AI-off boundaries.\n- The browser includes seven role/persona lenses mapped to the existing backend authority roles; the persona selector never grants new permissions.\n- A deterministic cross-domain journey summary automatically combines patient, logistics/planning, manufacturing, Lab/QC and Quality state and shows blocker, next owner and evidence count with AI disabled.\n- The UI exposes workflow automation for conflict detection/case creation, readiness evaluation, unknown-outcome reconciliation, duplicate-dispatch prevention, Quality evidence assembly and cross-domain summarization.
- A separate read-only source explorer renders exact frozen v2 `EVAL-001..006` patient assertions, six source-timestamp journey sequences and unresolved control gates with file/row provenance; the `INJ-001..010` preview derives hypothetical dependency impacts with zero side effects. The timestamp ordering is not known-at replay; neither view is a source migration, authoritative adjudication or committed re-plan.
- The off/fake-only assistant configuration is recorded in `assistant_config_registry.json`; no live provider or autonomous tool is selected.

## Verification

The 106-test suite covers inherited evidence integrity, domain/evaluation specifications, option spikes, contracts, foundation, three POCs, typed API validation/authentication/lifecycle, CLI behavior, source journey explorer/inject preview, end-to-end behavior, concurrent replay, assistant attacks, recovery and a local micro-benchmark. Exact test evidence and the registered load-test gap are recorded in Stage 15.

## Limits

External systems, authorities, identities and data are simulated. The API’s header principal is a demo mechanism, not production identity. There is no live model/provider, real patient data, validated e-signature, production infrastructure or independent assurance.
