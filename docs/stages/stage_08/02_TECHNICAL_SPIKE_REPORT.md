# Stage 8 - Technical Spike Report

**Status:** COMPLETE AS OPTION EVIDENCE; NOT A PRODUCTION IMPLEMENTATION

## Objective

Test whether the most important O2/O3 architectural properties can be expressed simply before committing to detailed architecture. The spike is in `docs/stages/stage_08/spikes/decision_kernel.py`; focused tests are in `tests/test_option_spikes.py`.

## Results

| Probe | Result | What it supports | What it does not prove |
|---|---|---|---|
| Canonical command digest and idempotency-key binding | PASS | Same command replays; changed payload conflicts | Durable/concurrent database semantics |
| Ambiguous adapter timeout | PASS | State becomes `OUTCOME_UNKNOWN`; no automatic retry | Real adapter reconciliation |
| MES/ERP release assertions | PASS | Cannot produce canonical Quality release | Complete QMS/e-signature validation |
| Authorized, evidence-bearing QMS event | PASS | Can produce `PRODUCT_RELEASED` in the probe | Production authority integration |
| Recorded-time cutoff with late valid-time evidence | PASS | Known-at history remains stable | Full projection engine performance |
| AI disabled | PASS | Deterministic context remains available | User experience quality |
| Model exception/outage | PASS | Falls back to deterministic context | Provider SLO or timeout behavior |
| Prohibited AI authority field | PASS | Output is rejected; no recommendation retained | Full prompt-injection resistance |
| Citation outside supplied evidence | PASS | Output is rejected | Semantic truth of cited evidence |

Focused spike suite result: **8 tests passed**. Option-scoring tests add three passes. Full clean capstone suite is recorded separately.

## Legacy comparison

The immutable baseline remains **2 passed and 3 expected failures**. The expected failures intentionally expose product-release equivalence, superseded point-threshold thermal logic and retry duplication. This is evidence against O1, not a criticism to be hidden by rewriting the source.

## Engineering conclusion

The deterministic safety kernel and bounded-AI failure boundary are feasible without microservices or multiple agents. The spike reduces architectural uncertainty only; Stage 9-13 must specify contracts and Stage 14 must implement durable behavior before Stage 15 can verify the catalog.
