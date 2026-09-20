# Stage 7 - Human Oversight and Review Protocol

**Status:** PROPOSED FOR ACADEMIC POC

## Principle

Human-in-the-loop is a real control only when the person has authority, competence, time, evidence, independence where required and a usable way to disagree. A decorative approve button is not oversight.

## Decision roles

| Decision | AI role | Required human authority | Independence requirement |
|---|---|---|---|
| Identity/lineage resolution | Extract, compare, summarize, propose | Identity Authority | Approver cannot derive authority from request payload; second review for high ambiguity |
| Milestone readiness | Explain deterministic prerequisite results | Named milestone authority | Missing controlled policy prevents approval |
| Slot/reservation command | Explain feasibility and impact | Authorized Planner | Requester/approver separation when policy requires |
| Deviation/QC/thermal disposition | Organize cited evidence only | Quality Authority | Enforced separation where applicable |
| Product release | No decision role | Quality release authority | AI and upstream systems cannot approve |
| Clinical readiness/action | No decision role | Authorized clinical role | Outside POC execution scope |

## Review sequence

1. Confirm authenticated role, scope and any separation-of-duties requirement.
2. Read the deterministic status and missing/contradictory evidence before AI text.
3. Open every material P0 citation; the interface records citation inspection.
4. Review uncertainty, policy version, effective time and alternative interpretation.
5. Choose approve, reject, request evidence, abstain or escalate; free-text approval alone is insufficient.
6. Re-authenticate or sign when the controlled policy requires it.
7. Record actor, authority, decision, evidence set, rule/policy version, rationale and time.
8. Verify the resulting event/effect or open an owned exception.

## Safe interface requirements

- Deterministic facts and AI recommendation are visually and structurally distinct.
- Uncertainty and missing evidence are not hidden in expandable text.
- Approval controls name the exact decision and payload.
- Reject, abstain and escalate are as accessible as approve.
- No pre-selected approval and no pressure countdown.
- Changed evidence invalidates stale recommendations and opens re-review.
- Keyboard access and non-color status cues are required for the POC UI.

## Human-factor evaluation

Use the same scenario pairs for rules-only Arm B and bounded-AI Arm C. Measure correctness, P0 error acceptance, evidence opened, time on task, override/abstain rate, confidence calibration and workload. Include deliberately fluent but wrong or incomplete recommendations. Passing requires zero accepted P0 trap recommendation, 100% material-evidence inspection and no safety degradation in C versus B.

## Insufficient oversight

The system must block or degrade when the role is unauthorized, the reviewer is also the prohibited requester, required evidence is unavailable, policy version is unknown, signature service is unavailable, workload prevents meaningful review or the reviewer declares a conflict. The exception receives a named owner and escalation timer.

Academic role simulation is labelled as simulation and cannot establish production competence or authorization.
