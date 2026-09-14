# Stage 15 - Residual Risk and TEVV Report Template

**Template status:** EMPTY - DO NOT INTERPRET AS TEST EVIDENCE

## Release candidate

- Version/commit:
- Build and dependency manifest:
- Configuration digest:
- Dataset and knowledge digests:
- Model/provider/version or AI disabled:
- Evaluation catalog digest:
- Execution environment and date:
- Test lead and reviewers:

## Executive verdict

- Overall: `NOT RUN | PASS | FAIL | INCONCLUSIVE`
- P0 outcome:
- P1 outcome:
- Open incidents:
- Recommended G4 decision:

## Results by evaluation layer

| Layer | Planned | Run | Pass | Fail | Inconclusive | Evidence link |
|---|---:|---:|---:|---:|---:|---|
| Static/specification | | | | | | |
| Unit/property | | | | | | |
| Contract | | | | | | |
| Integration/end-to-end | | | | | | |
| Fault/chaos/recovery | | | | | | |
| AI/red-team | | | | | | |
| Human factors | | | | | | |
| Performance/cost | | | | | | |

## P0 threshold evidence

Record numerator, denominator, raw evidence and exceptions for every P0 threshold in `01_EVALUATION_STRATEGY_AND_THRESHOLDS.md`. Never replace a failed P0 result with an average score.

## Arm comparison

| Metric | A baseline | B deterministic | C bounded AI | Interpretation/limits |
|---|---:|---:|---:|---|
| Correct resolution | | | | |
| P0 failures | | | | |
| Median task time | | | | |
| Evidence inspection | | | | |
| Override/abstention | | | | |
| p95 latency | | | | |
| Calls/tokens/cost | | | | |

## Failure and incident register

| ID | Case | Observed behavior | Severity | Root cause | Containment | Retest | Status |
|---|---|---|---|---|---|---|---|

## Residual-risk decisions

| Risk ID | Evidence | Actual residual | Accept/mitigate/avoid | Accountable owner | Rationale/expiry |
|---|---|---:|---|---|---|

## Claims permitted

List only claims directly supported by this run, with scope and denominator. Explicitly list claims that remain prohibited.

## Independent review

- Reviewer and independence basis:
- Review scope:
- Findings:
- Disposition:

Codex self-review is internal engineering evidence and is not independent assurance.
