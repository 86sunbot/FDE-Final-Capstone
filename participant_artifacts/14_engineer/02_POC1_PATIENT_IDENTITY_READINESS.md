# Stage 14 - POC1: Patient, Identity and Readiness

The POC registers source evidence without merging it, opens an owned P0 identity-conflict case, requires at least two corroborating evidence references for a proposal, binds approval to the exact proposal digest, enforces an Identity Authority role and applies an approved relation once. Replays do not create duplicate links.

Milestone readiness separately evaluates identity, consent, authorization and site evidence. `NOT_SATISFIED` and `UNKNOWN` fail closed; missing evidence cannot become satisfied. The view returns evidence IDs, blockers, unknowns and rule versions.

Implemented in `services/identity.py`, `services/readiness.py` and the shared evidence/case/storage modules. Verified by unit, integration, supplied identity/authority cases and the integrated demo.
