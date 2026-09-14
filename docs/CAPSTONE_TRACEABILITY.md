# CGT Capstone - Live Traceability Register

**Status:** Complete for the internal synthetic POC; external validation gaps retained  
**Machine-readable register:** `requirements/TRACEABILITY_MATRIX.csv`

## Traceability rule

Every consequential capability must maintain:

`Evidence -> Legacy lens/root cause -> Requirement/CTQ -> Rule/ADR -> Implementation -> Test/eval -> KPI -> Lifecycle decision`

Blank or `PENDING` cells are work to complete, not permission to infer a link. The register is updated at every material stage and frozen for G3.

## Current coverage

The register maps Stage 2 evidence through Stage 3 CTQs, Stage 5 rules, Stage 7 evaluation IDs, Stage 9–13 design, Stage 14 implementation, Stage 15 tests, Stage 19 measurements and the Stage 20 restrict/change decision. `VERIFIED_INTERNAL_POC` never means production validation.

## Status semantics

- `TRACED_TO_SPEC`: evidence is connected to an explicit domain/control specification.
- `PARTIAL`: one or more required downstream links are pending.
- `VERIFIED`: the complete chain has implementation and passing verification evidence.
- `ACCEPTED`: an accountable lifecycle decision references the verified chain.
- `VERIFIED_INTERNAL_POC`: the chain is implemented and tested on synthetic local evidence, with production assurance explicitly excluded.

All current rows are `VERIFIED_INTERNAL_POC`. Production, live-model, human-factor and independent assurance remain outside that status.
