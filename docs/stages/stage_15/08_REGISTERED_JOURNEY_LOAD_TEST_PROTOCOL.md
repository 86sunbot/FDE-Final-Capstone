# Stage 15 — Registered Journey-Projection Load Protocol and Open Verdict

**Verdict for build 1.2.0:** `NOT_VERIFIED`. The 5,000-iteration in-process readiness micro-benchmark is not the Stage 7 NFR test. No p95 result for the registered workload is asserted.

## Registered condition

Stage 7 requires an evidence-bearing deterministic **journey projection** over the fixed **27,507-row** synthetic source dataset, a warmed process, **20 concurrent clients**, and **p95 ≤ 250 ms**. Correctness, missing/contradictory evidence, provenance, trace/error metrics and partial-response behavior must be checked at the same time. The accepted command API separately has a p95 ≤ 1 s target excluding simulated provider delay.

## Executable gate once the target projection exists

1. Freeze dataset SHA-256, schema, source ownership and journey query contract. The current six-patient explorer and scripted POC are **not** a full-dataset journey projection.
2. Load all 23 source datasets; keep the original 132-file baseline immutable. Warm the server with recorded warm-up queries, then hold 20 clients on a mixed set of normal, identity-conflict, temporal-conflict, withdrawn-consent, Quality-unknown and inject-preview journeys. Declare duration, arrival rate, hardware and cache settings before running.
3. Capture per-request wall latency (p50/p95/p99), server spans, errors/timeouts, response size, evidence counts and CPU/memory. Store raw traces and the histogram with the exact release manifest and dataset digest.
4. Independently compare each response with a golden decision record: no invented identity edge, no omitted evidence, no unauthorized release, explicit unknown and no partial projection presented as ready.
5. Repeat AI `off`; if a live provider is later approved, separately measure model latency/timeout/fallback without allowing it to block deterministic safety state.
6. A failed correctness/P0 gate fails the NFR regardless of latency. A micro-benchmark, one-client probe or different data volume cannot be substituted. Obtain TEVV/SRE and independent reviewer approval before changing `NOT_VERIFIED`.

**Why open:** the current application has three scripted POCs and read-only source-case/preview views, but not the specified fully ingested 27,507-row governed projection endpoint or 20-client runner. This is a product gap, not a hidden test pass. Trace: Stage 7 `01_EVALUATION_STRATEGY_AND_THRESHOLDS.md`, `EXT-PERF-001`, Stage 13 `REQ-PERF-001` (local micro-target only), Stage 20 G-07/G-10.
