# Stage 2 - AntiGravity Prototype Reuse Disposition

**Audited revision:** `143a48c33d9be718ccc48d40a9637403c8818caf`  
**Status:** Component-level recommendation; revalidate if upstream changes  
**Last updated:** 2026-09-14

## Decision principle

Reuse ideas and evidence only where verified. Do not inherit claims, duplicated data, disconnected workflow rules or placeholder artifacts. The safest implementation path is a clean Codex-controlled solution tree that imports explicitly approved assets.

## Component disposition

| Component | Disposition | Rationale | Required action |
|---|---|---|---|
| README proof-of-concept disclaimer | Reuse with revision | Corrects prior production overclaim | Align with final architecture and actual commands |
| Original challenge data subset | Reject as baseline | Incomplete and duplicated into contradictory databases | Use verified full 132-file extraction from original ZIP |
| Forensic script | Rewrite/extend | Reproduces only a small subset | Use `capstone/tools/forensic_baseline.py` as current source |
| Engagement and discovery prose | Mine selectively | Captures some valid themes | Replace with Stage 1/2 evidence-backed artifacts |
| 180 generic exhaustive artifacts | Reject/remove from final | Filenames do not establish delivery | Produce only substantive stage artifacts |
| `domain.py` state enum | Reject | Conflicts with implemented state machine and domain requirements | Define one canonical model in Stage 5 |
| `state_machine.py` | Rewrite | Useful SQLite transition proof but applies release gate at wrong transition and lacks authority/bitemporal semantics | Specify/test state model before new implementation |
| `safety_gates.py` | Mine tests/ideas | Improved fail-closed intent but consent vocabulary and thermal thresholds are not controlled by evidence | Derive rules from approved decision models/SOPs |
| `slot_service.py` | Reject | In-memory, untested and not payload-safe or concurrent | Build persistent idempotent command service |
| Three workflow scripts | Reject as POCs; keep as cautionary examples | Separate SQL/rules, divergent DB, tests only check exit code | Build shared-service vertical slices |
| FastAPI orchestration API | Rewrite | No authentication/authorization; self-asserted roles accepted; spec mismatch | Generate from approved contracts and policy |
| Mock MES/QMS server | Rewrite selectively | Useful adapter concept but consent endpoint fails and deviation closure is unauthenticated | Contract-test safe mock adapters |
| Agent implementation | Rewrite | Injection detection not integrated; context PHI not scrubbed; weak validation; live behavior unevaluated | Build bounded adapter after Stage 11 specification |
| Streamlit UI | Redesign | Demonstration value but hard-coded/simulated authority and duplicated logic | UI must call shared APIs and show evidence/uncertainty |
| OpenAPI sketch | Reject/replace | Does not match implementation or full domain | Create versioned canonical APIs/events in Stages 9-13 |
| ADR document | Reuse format selectively | Some context/consequence structure | Re-evaluate decisions with alternatives, owners and verification |
| Traceability matrix | Reject/replace | Requirement identifiers map to wrong meanings | Build machine-verifiable bidirectional traceability |
| Unit tests | Mine edge cases | Thirty tests pass but coverage and workflow assertions are weak | Rebuild from Stage 7 evaluation requirements |
| TEVV harness | Reject as assurance; reuse attack seeds | Three regex cases do not evaluate an agent/system | Use original six evals, ten injects and expanded harness |
| Docker assets | Rewrite | Useful packaging direction but configuration is ignored and healthcheck depends on absent `curl` | Build/test after target architecture |
| 30/60/90 roadmap | Reuse structure | Honest gap categories | Recalculate after verified implementation/readiness assessment |
| Value report | Reuse hypotheses only | Correctly relabels some claims | Replace with measured POC results and explicit financial assumptions |
| AIMS report | Reject/replace | Still contains unsupported post-deployment/audit/latency claims | Produce internal lifecycle review from actual evidence |

## Reuse gate

Before importing any prototype component:

1. Link it to an approved requirement and ADR.
2. Add a failing test that demonstrates the relevant inherited defect or gap.
3. Verify it uses the canonical domain and contracts.
4. Verify it cannot mutate immutable evidence.
5. Verify authorization and audit boundaries.
6. Record reuse, rewrite or removal in traceability.

## Recommendation

Treat the AntiGravity repository as an architectural sketch and defect-learning resource. Do not continue adding files to it until the Stage 13 build-ready baseline is approved. Build the final integrated implementation from the verified challenge evidence and new specifications.
