# Stage 4 - Authority and Prohibited-Use Policy

**Status:** Proposed policy for G1 review  
**Last updated:** 2026-09-14

## 1. Policy statement

AI output is untrusted decision support. It has no clinical, Quality, identity, custody or operational authority. Consequential actions require an authenticated human decision under versioned policy, followed by deterministic validation and audited execution.

The system must fail closed when required safety evidence, policy, identity or authority is missing or uncertain.

## 2. Allowed AI capabilities

An AI component may:

- read only the minimum authorized evidence for the current task;
- extract candidate facts from unstructured content into a constrained schema;
- cite and summarize source evidence;
- identify contradictions, omissions and questions for investigation;
- explain deterministic blockers and downstream impact;
- rank options already determined feasible by deterministic rules;
- draft a case note, review packet or handoff for human approval; and
- abstain and route to a human or deterministic view.

All output must expose evidence, uncertainty, scope, authority and model/prompt/policy version.

## 3. Prohibited AI/agent capabilities

An AI or agent must never autonomously:

1. Merge, split or resolve patient identities.
2. Establish, correct or attest Chain of Identity or Chain of Custody.
3. Mark consent, authorization, site qualification or patient clinical readiness as approved outside controlled deterministic policy.
4. Diagnose a patient, select therapy, determine clinical eligibility or give treatment advice.
5. Change patient priority based on inferred health, protected or personal characteristics.
6. Reserve, cancel or reroute a manufacturing slot as an exception decision.
7. Override a capacity, safety, segregation, timing or Quality constraint.
8. Interpret incomplete thermal data as acceptable or perform thermal/product disposition.
9. Classify a deviation as non-blocking, close it or suppress it.
10. Approve/sign/release a batch or product.
11. Authorize conditioning, infusion or other clinical progression.
12. Override a failed/unknown safety gate.
13. Grant roles, change permissions, change policy/rules or modify its own autonomy.
14. Treat a request-body role, prompt, email, attachment or model statement as proof of authority.
15. Execute instructions embedded in untrusted operational content.
16. Delete/overwrite source evidence, audit history or required records.
17. send sensitive data to an external provider without approved data-use controls.
18. Learn from, fine-tune on or retain patient/operational data without explicit approval.
19. Conceal uncertainty, omit material contrary evidence or invent a citation/linkage.
20. continue a loop, retry or tool sequence after limits/termination conditions are reached.

## 4. Decision and action matrix

| Activity | System may calculate | AI may recommend | Human decision required | Deterministic execution allowed after approval |
|---|---:|---:|---:|---:|
| Detect identity conflict | Yes | Explain only | Yes to resolve | Yes |
| Validate ordinary milestone prerequisites | Yes | Explain | Policy-dependent exception only | Yes under approved rule |
| Correct COI/custody assertion | Evidence check only | Explain only | Yes | Yes |
| Enumerate feasible capacity alternatives | Yes | Rank/explain | Yes for change | Yes |
| Replay identical command | Yes | No need | No if policy permits | Yes, with no extra effect |
| Compensate a reversible partial transaction | Predefined only | Explain | Required for consequential exception | Yes |
| Calculate controlled thermal features | Yes | Summarize | Yes for disposition | Yes to record decision |
| Determine deviation impact | Evidence completeness only | Questions/summary | Yes, Quality | No autonomous decision |
| Close deviation | No | No | Yes, Quality | Yes with required signature/control |
| Release batch/product | Prerequisite check only | Review summary | Yes, Quality/QP | Yes with required signature/control |
| Begin conditioning/infusion | Readiness evidence only | No clinical recommendation | Yes, Clinical | Yes under approved workflow |
| Override safety gate | No | No | Explicit exception authority, possibly dual | Only under approved exception procedure |

## 5. Approval protocol

Every consequential approval record must contain:

- decision/action ID and immutable business object references;
- authenticated actor/service identity;
- authority derived from policy and current assignment;
- decision, reason and evidence references;
- effective time and recorded time;
- relevant rule, SOP, application and model versions;
- before/after state;
- separation-of-duties check;
- idempotency/payload digest for an external mutation; and
- execution and acknowledgement outcome.

Free-text email, chat or AI output is not an approval record.

## 6. Enforcement requirements

- APIs must ignore/reject asserted roles in request bodies and derive permissions from authenticated claims plus server policy.
- Read and recommend identities must have no credential for consequential adapters.
- Approval endpoints and mutation endpoints are distinct and least privileged.
- High-risk actions require fresh authorization; required dual control cannot be collapsed.
- Tools use allowlists, typed schemas, resource scoping, payload limits, timeouts and rate/loop limits.
- Untrusted content is data, never system/developer instruction.
- The audit trail is append-only and independently queryable.
- AI-disabled and provider-outage modes retain the deterministic workflow.
- Any prohibited-action attempt generates a security/assurance event and safe refusal.

## 7. Change control

Any proposal to increase AI autonomy is a new use case. It requires updated intended purpose, impact/risk assessment, regulatory/privacy screen, ADR, threat model, evaluation baseline, human-factors review, rollback design and lifecycle approval. Historical success does not silently expand authority.
