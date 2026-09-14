# Stage 13 - Final Academic Build ADRs

| ADR | Decision | Status | Verification |
|---|---|---|---|
| ADR-001 | Clean tree; immutable baseline | ACCEPTED | Integrity test |
| ADR-002 | Modular monolith with enforced package boundaries | ACCEPTED | Import/component tests |
| ADR-003 | SQLite transactional POC store behind ports | ACCEPTED | Migration/integration/recovery tests |
| ADR-004 | Source assertions plus evidence-bearing projections | ACCEPTED | Evidence and temporal tests |
| ADR-005 | Versioned legal state transitions; unknown fails closed | ACCEPTED | Domain/readiness tests |
| ADR-006 | Server-side principal/role/scope and separate approval event | ACCEPTED | Authorization tests |
| ADR-007 | Payload-bound idempotency and reconcile-before-retry | ACCEPTED | Command tests |
| ADR-008 | One optional read/recommend assistant; AI off by default | ACCEPTED | Assistant/adversarial tests |
| ADR-009 | No multi-agent, vector database or long-term model memory | ACCEPTED | Architecture inspection |
| ADR-010 | Audit hash chain and correlation on controlled actions | ACCEPTED | Audit integrity tests |
| ADR-011 | Simulation adapters for external effects | ACCEPTED | Contract/fault tests |
| ADR-012 | Frozen evaluation catalog; results separate from specifications | ACCEPTED | Evaluation validator |

These ADRs are final for the academic build but not production technology decisions.
