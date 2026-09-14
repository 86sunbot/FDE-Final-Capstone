# Stage 4 - Value, Risk, Feasibility and G1 Decision Proposal

**Status:** Decision proposal; accountable human approval pending  
**Last updated:** 2026-09-14

## 1. Assessment scale

Ratings are qualitative triage, not Stage 7 risk scores:

- **Value:** expected operational/safety contribution if the hypothesis is true.
- **Inherent consequence:** severity if the capability is wrong or misused before controls.
- **Feasibility:** ability to implement and evaluate within the supplied synthetic capstone.
- **Decision:** `GO`, `CONDITIONAL GO` or `NO-GO` for capstone evaluation.

## 2. Value-risk-feasibility matrix

| Candidate | Value | Inherent consequence | Feasibility | Evidence/rationale | Decision |
|---|---|---|---|---|---|
| Shared deterministic evidence/orchestration platform | High | High | High | Addresses readiness, event, idempotency, authority and case root causes; required even without AI | **GO** |
| UC-01 deterministic identity-conflict/readiness workflow | High | Critical | High | Directly covers duplicated/disagreeing identity evidence and omitted gates; can abstain safely | **GO** |
| UC-01 AI conflict/evidence summary | Medium | High | Medium | May reduce review time, but wrong framing could bias identity resolution | **CONDITIONAL GO**: cite all evidence; no merge/action permission |
| UC-02 deterministic constraint/idempotency/recovery workflow | High | High | High | Directly covers retry duplicates, partial transactions and slot conflict | **GO** |
| UC-02 AI explanation/ranking of feasible alternatives | Medium | High | Medium | Possible coordination benefit after deterministic feasibility; priority fairness and action risk remain | **CONDITIONAL GO**: human selection; no write tools |
| UC-03 deterministic Quality/thermal evidence packet and gate | High | Critical | High | Prevents manufacturing/ERP substitution for release and exposes missing disposition evidence | **GO** |
| UC-03 AI evidence-packet summary | Medium-to-high | Critical | Medium | High information burden, but omission/hallucination could affect review | **CONDITIONAL GO**: Quality review, citations, unknowns, no disposition/release |
| Predictive release/ETA model | Unproven | Medium/high | Low-to-medium | Ground truth, feature lineage and reproducible outcome definition are not yet established | **NO-GO now**; reconsider after Stages 6-8 |
| Autonomous identity, deviation, release or clinical decision | None acceptable | Critical | Technically possible but impermissible | Conflicts with authority, safety and challenge constraints | **NO-GO** |
| Autonomous multi-agent operational control | Unproven | Critical | Low | Adds handoff, loop, authority and failure complexity without demonstrated need | **NO-GO** |

## 3. Proposed solution boundary for G1

Approve three integrated use cases on one shared deterministic platform:

1. Patient/identity readiness.
2. Manufacturing disruption and slot orchestration.
3. Product/QA/thermal-release support.

For each use case, approve deterministic evidence/rule/workflow engineering. Permit a replaceable AI adapter only for non-authoritative extraction, summary, explanation or recommendation, subject to Stage 7 thresholds and Stage 8 comparison.

## 4. G1 go criteria

G1 may be approved when accountable reviewers accept that:

- the Stage 1 mandate, users, affected groups and decision owners are correct;
- Stage 2 evidence accurately represents the supplied brownfield estate;
- Stage 3 problem, root causes, baselines and success/kill criteria are suitable;
- the intended purpose and exclusions are frozen for the capstone;
- Legal/Regulatory/Quality/Privacy uncertainties are recorded rather than falsely resolved;
- the three use cases are valuable, feasible and testable;
- deterministic and AI responsibilities are separated;
- prohibited use and human authority are explicit; and
- no production, validation, compliance or independent-assurance claim is made.

## 5. G1 no-go/rework criteria

Return to the relevant earlier stage if:

- a reviewer cannot identify who owns a consequential decision;
- intended purpose includes clinical advice or autonomous Quality/identity/custody action;
- the solution assumes one global source of truth or erases contradictory evidence;
- baseline findings or metrics cannot be reproduced;
- real personal data/provider use is introduced without Privacy/Security approval;
- a regulatory classification is asserted without actual deployment/record/use facts;
- the rules-only baseline is removed; or
- the selected scope cannot be tested with explicit acceptance criteria.

## 6. Decision requested

**Recommended G1 outcome:** `CONDITIONAL APPROVAL TO PROCEED TO STAGES 5-8`, subject to:

1. The Capstone Owner confirming the academic POC intended purpose, audience and final format.
2. Human review of the Stage 1-4 evidence package.
3. Regulatory/Legal/Quality/Privacy conclusions remaining labelled preliminary and out-of-scope for formal certification.
4. No expansion of AI authority beyond `04_AUTHORITY_AND_PROHIBITED_USE_POLICY.md`.
5. G2 requiring measured comparison of rules-only and bounded-AI variants.

Until the accountable owner records the decision, G1 remains `READY FOR REVIEW`, not approved.
