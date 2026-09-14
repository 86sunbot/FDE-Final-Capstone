# Stage 16 - Incident, Change and Recovery Plan

| Severity | Example | Response |
|---|---|---|
| P0 | Wrong identity/release, unauthorized action, duplicate effect, audit failure | Stop affected mutation, contain, preserve evidence, owner immediately, no reopen without full P0 rerun |
| P1 | Owned outage, performance breach, repeated AI rejection | Degrade safely, assign, diagnose and retest |
| P2 | Cosmetic/read-only issue | Backlog with evidence |

Changes to rules, schemas, authority, event transitions, command semantics, assistant contract, model/provider or data classification trigger impact analysis and targeted plus full P0 regression. Emergency changes are not exempt from after-the-fact evidence/CAPA.

The completed local recovery drill achieved a matching state digest, valid audit chain and recovery below the 60-second academic target. This measures a temporary SQLite fixture only; production RTO/RPO remain undefined.
