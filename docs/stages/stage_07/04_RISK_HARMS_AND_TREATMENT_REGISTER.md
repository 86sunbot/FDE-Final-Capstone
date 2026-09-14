# Stage 7 - Risk, Harm and Treatment Register

**Status:** READY FOR REVIEW; residual risk is not yet accepted

## Scoring

Likelihood and impact use 1 (low) to 5 (very high). Score is likelihood multiplied by impact. Bands are Low 1-4, Medium 5-9, High 10-16 and Critical 17-25. Scores support prioritization; a low score never permits a prohibited action.

| ID | Harm scenario | Initial LxI | Key preventive/detective treatment | Evaluation evidence | Target residual | Accountable role |
|---|---|---:|---|---|---:|---|
| R7-01 | Incorrect identity/lineage association affects the wrong journey | 4x5=20 | Namespace identifiers, multi-source corroboration, proposal/approval/apply split | EVAL-002; INJ-007; EXT-ID-001..003 | <=5 and no P0 failure | Identity Authority |
| R7-02 | Missing/withdrawn consent or authorization is ignored | 3x5=15 | Milestone-specific gate, temporal re-evaluation, fail closed | EVAL-004; INJ-010; EXT-GATE-001..003 | <=5 | Clinical/Commercial Authority |
| R7-03 | Expired site qualification permits progression | 3x5=15 | Attribute-level readiness, effective-time validation | INJ-005; EXT-GATE-004 | <=5 | Site Qualification Owner |
| R7-04 | MES/ERP or AI substitutes for Quality release | 4x5=20 | Source-specific authority, signed ProductReleased event, no AI authority | EVAL-005..006; INJ-009; EXT-QUAL-001..003 | <=5 and no P0 failure | Quality Authority |
| R7-05 | Ambiguous QC/thermal evidence causes wrong disposition | 4x5=20 | Preserve raw evidence, abstain, require owned Quality review | INJ-002; INJ-004; EXT-QUAL-004..005 | <=8 and no autonomous disposition | Quality Authority |
| R7-06 | Superseded or draft knowledge is treated as effective policy | 3x4=12 | Version/effective-date retrieval and trust-tier labels | EXT-GATE-003; EXT-QUAL-006 | <=4 | Document/Policy Owner |
| R7-07 | Late or contradictory events rewrite history | 4x4=16 | Occurred/recorded time, immutable decisions and bitemporal replay | EVAL-003; EXT-TIME-001..002 | <=4 | Data Owner |
| R7-08 | Retry or concurrency creates duplicate reservation/effect | 4x5=20 | Semantic idempotency, outbox and canonical payload binding | INJ-006; EXT-CMD-001..002 | <=5 and zero duplicates | Service Owner |
| R7-09 | Unknown/partial external outcome is retried unsafely | 4x5=20 | OUTCOME_UNKNOWN, reconciliation before retry, verified compensation | EXT-CMD-003..004 | <=5 and zero blind retries | Service Owner |
| R7-10 | Unauthorized or same-person approval changes state | 3x5=15 | Authenticated server policy and separation of duties | EXT-AUTH-001..003; EXT-SEC-001 | <=5 | Security/Business Authority |
| R7-11 | Prompt injection causes policy bypass or release action | 4x5=20 | Untrusted-content isolation, allowlisted read-only tools, structural authority boundary | EVAL-006; EXT-AI-001 | <=5 and zero tool effects | AI/Security Owner |
| R7-12 | Sensitive data leaks through prompt, output or logs | 3x5=15 | Deny external AI, minimization, DLP/redaction and scoped access | EXT-AI-002; EXT-SEC-001 | <=5 | Privacy/Security Owner |
| R7-13 | Hallucination, omission or conflict misleads a reviewer | 4x5=20 | Evidence-bound schema, deterministic view, citation/coverage checks, abstention | EXT-AI-003..004; EXT-AI-006; EXT-HUM-001 | <=8 and no P0 acceptance | AI/Quality Owner |
| R7-14 | Model/dependency outage or loop removes service availability | 4x4=16 | Deterministic fallback, timeouts, attempt limits and owned recovery | EXT-AI-005; EXT-AI-007; EXT-REC-001 | <=4 | Operations Owner |
| R7-15 | Audit evidence is altered, incomplete or not attributable | 3x5=15 | Append-only records, actor/source/time/correlation, digests and access controls | EXT-SEC-002; EXT-REC-001 | <=5 | Assurance/Security Owner |
| R7-16 | Human over-relies on AI or cannot safely override it | 4x5=20 | Rules-only view, evidence inspection, trap cases, override/escalation workflow | EXT-HUM-001..002 | <=8 and no P0 acceptance | Product/Human Factors Owner |
| R7-17 | Synthetic POC metrics are represented as production benefit or compliance | 4x4=16 | Claim labels, denominators, limitation banner and approval gate | CTQ-010 review; Stage 19 claim audit | <=4 | Capstone Owner |

## Treatment decision rules

- P0 prohibited outcomes are not accepted through score reduction.
- Residual scores are targets until testing demonstrates the control and an accountable owner records acceptance.
- Transfer to a provider does not transfer organizational accountability.
- A missing policy, owner or evidence source keeps the decision unknown or blocked.
- New incidents, intended-use changes, real data or consequential integrations reopen the relevant risk assessment.
