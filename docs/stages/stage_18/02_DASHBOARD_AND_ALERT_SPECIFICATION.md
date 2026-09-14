# Stage 18 - Dashboard and Alert Specification

## Safety panel

- unauthorized accepted actions (target zero);
- identity proposals/approvals/links and stale proposals;
- Quality releases by authority and evidence completeness;
- illegal/rejected transitions;
- duplicate effects and idempotency conflicts;
- unknown outcome age and owner;
- unowned P0 cases;
- audit-chain verification.

## Service panel

- request/command latency and error rate;
- source freshness and schema/volume/null/relationship drift;
- adapter outage and reconciliation duration;
- backup age, restore result and RTO/RPO;
- open cases by severity, owner and age.

## AI panel

- mode/model/version/provider;
- calls, latency, tokens and cost when applicable;
- schema/citation/injection rejection and fallback rate;
- recommendation override/abstention and evidence inspection;
- Arm B/C correctness and task time.

P0 alerts stop or isolate the affected mutation path. AI alerts disable AI without disabling deterministic service.
