# Stage 13 - Build-Ready Specification

**Status:** APPROVED FOR SYNTHETIC ACADEMIC BUILD

## Product increment

Build one local modular monolith with:

1. evidence/assertion and bitemporal projection foundation;
2. server-side role/scope authorization and tamper-evident audit;
3. persistent commands, semantic idempotency and reconciliation;
4. owned exception cases;
5. POC1 identity and milestone readiness;
6. POC2 simulated slot reservation/recovery;
7. POC3 Quality evidence packet and authorized release;
8. optional provider-neutral bounded assistant, disabled by default;
9. CLI/API demo, telemetry, evaluation runner, backup/restore and release manifest.

## Definition of done

- All requirements in `requirements/requirements.csv` have implementation and test evidence.
- Three POCs use the same database, audit, authorization, evidence and service layer.
- No P0 test fails; inconclusive human/live-model/production evidence is labelled.
- The source ZIP and verified extraction remain unchanged.
- Local setup, tests, demo, evaluation, backup/restore and teardown are documented.
- Final lifecycle decision is evidence-based and does not claim production readiness.

## Technology constraints

Core behavior uses Python 3.11+ standard library and SQLite. FastAPI/Uvicorn are optional API dependencies. No live model, external system, credential or real data is required. Deterministic IDs/timestamps may be injected for tests.
