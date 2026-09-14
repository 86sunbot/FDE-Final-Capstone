# Stage 8 - Reference, Model and Provider Comparison

**Status:** ARCHITECTURAL COMPARISON; NO PROVIDER PROCURED OR APPROVED

## Reference-pattern comparison

| Pattern | Safety clarity | Capstone feasibility | Evaluation value | Decision |
|---|---|---|---|---|
| CRUD over legacy tables | Low | High superficially | Low | Reject |
| Deterministic domain core with evidence projections | High | High | High | Required foundation |
| Event-driven distributed services | Potentially high | Low | Medium | Defer |
| Retrieval chatbot over all documents | Low | Medium | Medium | Reject |
| Evidence-bound recommendation adapter over deterministic context | High if enforced structurally | Medium-high | High | Include behind flag |
| Autonomous/multi-agent workflow | Low for current evidence | Low | High demo novelty, low decision value | Reject |

## Model/provider profiles

| Profile | Strength | Main risk | POC position |
|---|---|---|---|
| AI disabled / deterministic only | Lowest new AI risk and cost | Less natural-language assistance | Default and mandatory fallback |
| Local deterministic fake/stub | Repeatable schema/failure testing | Not evidence of model quality | Use in CI and most engineering tests |
| Local open-weight model | Data locality and lower provider dependency | Hardware, patching, evaluation and model-quality burden | Optional later experiment only |
| Hosted small model | Potentially lower latency/cost | Data transfer, provider dependency and quality variance | Eligible only after approval and measurement |
| Hosted frontier model | Stronger general reasoning potential | Privacy, cost, variability and lock-in | Eligible only for bounded comparison after approval |

## Selection rule

Stage 8 selects a **provider-neutral adapter**, not a named model. CI uses a deterministic fake. Any live model trial requires an approved provider/model/version, credentials outside the repository, synthetic-only prompt policy, timeout/token limits, structured-output validation and recorded calls/cost. No provider is allowed to receive real patient or health data within this capstone.

A current vendor comparison and price quote are intentionally deferred because no procurement geography, service terms, security requirements or approved budget is supplied. Those facts must be researched at the date of a real decision rather than guessed here.
