# Stage 14 - POC2: Manufacturing Disruption and Slot Orchestration

An authorized Planner submits a canonical patient/slot command with an idempotency key. The database binds that key to command type, scope and payload digest before the simulated adapter executes. Identical replay returns the stored state without dispatch; changed payload returns `IDEMPOTENCY_CONFLICT`.

A timeout after a simulated successful effect becomes `OUTCOME_UNKNOWN`. Reconciliation queries recorded external state before changing to success; no blind retry occurs. Partial effects become `COMPENSATION_PENDING` and require explicit verified compensation.

Implemented in `services/commands.py` and `adapters/slot_simulator.py`. Verified for success, replay, conflict, concurrency, timeout-after-success, reconciliation and compensation.
