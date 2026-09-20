# Stage 8 - Weighted Trade-off and Selection

**Status:** RECOMMENDATION FOR G2

The reproducible input is `option_scores.json`; `tools/score_solution_options.py` checks that weights total 100, validates the score scale and writes `option_scores.csv`.

## Criteria

Safety/authority has the largest weight (25%). Problem/capstone fit is 15%; evidence/traceability and implementation feasibility are 10% each; operability, time and AI-off reversibility are 8% each; lock-in, TCO confidence, extensibility and evaluation/learning are 4% each. A weighted score cannot rescue an option that fails the safety threshold.

## Result

| Rank | Option | Score / 5 | Safety screen | Disposition |
|---:|---|---:|---|---|
| 1 | O3 deterministic core + one bounded optional assistant | 4.70 | Pass hypothesis; Stage 15 proof pending | Recommend |
| 2 | O2 clean rules-only modular monolith | 4.58 | Pass hypothesis; Stage 15 proof pending | Required fallback |
| 3 | O6 full distributed rebuild | 3.92 | Pass hypothesis; excessive scope | Reject for capstone |
| 4 | O5 buy/partner SaaS | 2.33 | Unproven | Defer production scan |
| 5 | O4 agent-first multi-agent | 2.28 | Fail | Reject |
| 6 | O1 patch inherited prototype | 2.17 | Fail | Reject |

## Why O3 wins narrowly

O3 contains O2 intact and adds a replaceable assistant solely to test incremental FDE value. Its complexity penalty is accepted because the capstone specifically needs to demonstrate disciplined AI use and compare rules-only with AI-assisted work. The choice is reversible: if the assistant cannot pass Stage 15 or show Stage 19 value, disable it and the selected platform behaves as O2.

## Trade-offs accepted if G2 approves

- One deployable modular monolith before distributed services.
- One assistant before any multi-agent design.
- Deterministic evidence and workflow before model convenience.
- Local synthetic simulation before real integration.
- Explicit unknowns before invented policy.
- Provider neutrality before model optimization.
- Measured AI increment before any AI value claim.
