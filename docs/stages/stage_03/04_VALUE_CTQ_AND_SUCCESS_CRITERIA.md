# Stage 3 - Value Hypotheses, CTQs and Success/Failure Criteria

**Status:** Hypotheses for evaluation; not achieved outcomes  
**Last updated:** 2026-09-14

## 1. Primary value hypothesis

If the enterprise introduces a deterministic, evidence-preserving orchestration and exception layer with authenticated human authority, then it can reduce unsafe readiness conclusions, reconciliation effort, duplicate/conflicting actions and exception delay while improving traceability and recovery.

If bounded AI is added only for evidence extraction, summarization, impact explanation and alternative recommendation, then operator task time may improve without increasing unauthorized action, hallucinated linkage, automation bias or privacy exposure.

The deterministic-layer hypothesis and AI-increment hypothesis will be measured separately.

## 2. Critical-to-quality requirements

| CTQ ID | Critical-to-quality outcome | Why critical | Evidence of success |
|---|---|---|---|
| CTQ-001 | Correct patient/material/batch linkage or explicit abstention | Therapy is individualized | No invented link; source/conflict/confidence and human resolution visible |
| CTQ-002 | Manufacturing completion never substitutes for QA release | Quality authority is consequential | P0 transition tests and policy evidence |
| CTQ-003 | Consent/site/authorization prerequisites are milestone-specific and revalidated | Upstream facts can invalidate plans | Versioned gate evidence and negative tests |
| CTQ-004 | Quality disposition remains human-authorized | Release/disposition cannot be autonomous | Authenticated approval and immutable audit test |
| CTQ-005 | Commands are idempotent, payload-bound and recoverable | Retried distributed work must not duplicate effects | Replay, conflict, concurrency and compensation tests |
| CTQ-006 | Event state is bitemporal and reproducible | Late/out-of-order data changes current knowledge | Deterministic replay at valid/recorded time |
| CTQ-007 | Every recommendation exposes evidence, uncertainty and authority | AI output must be reviewable | Schema and grounding evals |
| CTQ-008 | Critical exceptions have accountable ownership and escalation | Unowned work creates hidden delay/risk | Case/SLA tests and monitoring |
| CTQ-009 | System degrades safely without AI or an unavailable source | Cloud/dependency failure is expected | Outage and recovery tests |
| CTQ-010 | Results and claims are reproducible and honestly classified | Capstone credibility depends on evidence | Clean-run manifest and claim audit |

## 3. Value tree

| Value branch | Mechanism | Expected evidence | Counter-risk |
|---|---|---|---|
| Patient/product safety | Explicit gates and authority | Zero P0 safety violations in golden/failure tests | Excessive false blocks delaying treatment |
| Quality/assurance | Provenance, decisions and signatures | Complete audit/evidence packages | Administrative burden |
| Speed | Shared case view and bounded summaries | Reduced task and exception-resolution time in simulation | Automation bias or poor recommendations |
| Capacity | Idempotent slot orchestration and alternatives | No duplicate reservation; improved simulated utilization | Unfair or clinically inappropriate prioritization |
| Resilience | Known degraded modes and compensation | Recovery within tested objectives | Manual workaround overload |
| Data trust | Conflict visibility and bitemporal reconstruction | Higher traceability and fewer unexplained states | False confidence in canonical projection |
| Cost | Reduced reconciliation and avoidable delay | Cost-to-value model with explicit assumptions | Model/operational cost exceeds benefit |

## 4. Counter-metrics

| Counter-metric | Harm prevented | Trigger for review |
|---|---|---|
| False-block rate on approved normal cases | Treatment delay from over-conservative gates | Any P0 normal case blocked incorrectly |
| Time awaiting human approval | Excess workflow delay | Exceeds stage-specific SLO |
| Human recommendation rejection rate | Low AI usefulness | Sustained rate outside Stage 7 threshold |
| Override/workaround rate | Poor workflow fit or hidden risk | Increase versus shadow baseline |
| Critical alert volume per operator | Alert fatigue | Exceeds tested capacity |
| Unowned critical-case duration | Accountability failure | Any critical case beyond assignment SLO |
| Evidence omitted from recommendation | Automation bias/false confidence | Any P0 recommendation lacks required evidence |
| Privacy/DLP escape rate | PHI disclosure | Any confirmed PHI escape |
| Model/tool cost per successful case | Negative economics | Exceeds approved cost ceiling |
| Disparate delay/false-block rate by site/region | Unequal operational impact | Material unexplained difference |
| Recovery manual steps | Fragile operations | Exceeds runbook assumption or staffing capacity |

## 5. Capstone success criteria

The capstone succeeds when:

1. The evidence baseline and all material findings reproduce from a clean environment.
2. One canonical domain, event and state model is used across the three workflows.
3. The three POCs operate through shared APIs/services and never mutate the immutable baseline.
4. All six supplied evaluation cases and ten failure injections execute against the integrated solution.
5. All P0 deterministic, authority, privacy and recovery tests pass.
6. No AI/agent can directly perform a consequential mutation.
7. Human approvals are authenticated, authorized, reasoned and auditable.
8. AI-disabled operation remains usable and safe.
9. Before/after results and cost assumptions are reproducible.
10. Residual risks and production gaps are explicit.
11. A clean clone runs using documented commands without cloud credentials.
12. The final recommendation is conditional on the evidence actually achieved.

## 6. Kill/failure criteria

Stop or return to an earlier phase if any of the following remains true:

- A POC invents an identity, COI, shipment, batch or product linkage.
- Manufacturing/ERP state can bypass Quality release authority.
- Missing evidence is interpreted as safe.
- An unauthenticated/self-asserted role can approve or execute consequential action.
- A retry can create duplicate side effects or silently reuse a key for a different payload.
- Untrusted email/document content can become agent instruction or executable action.
- The system cannot run safely with the AI provider disabled.
- Baseline evidence is mutated or cannot be reproduced.
- P0 tests are missing, skipped or failing.
- Critical residual risk lacks an accountable human owner.
- A report presents a target, simulation or hypothesis as production fact.

## 7. Value-validation sequence

1. Stage 6 defines reproducible formulas for supplied business KPIs where possible.
2. Stage 7 defines thresholds, samples and statistical/qualitative evaluation methods.
3. Stage 8 compares no-AI, deterministic and AI-assisted options.
4. Stage 14 instruments the three workflows.
5. Stage 15 measures task, safety, authority and reliability outcomes.
6. Stage 17/18 collect shadow/canary simulation evidence.
7. Stage 19 calculates before/after variance, counter-metrics and cost-to-value.

Until this sequence is complete, all benefits remain hypotheses.
