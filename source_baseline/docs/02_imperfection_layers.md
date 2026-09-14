# 11 Layers of Inherent Brownfield Imperfection

## L1 — Software / Code
Legacy code, defects, duplication, hard-coded rules, obsolete frameworks, weak tests and configuration debt.

## L2 — System / Integration
APIs, databases, schemas, events, interfaces, distributed-state failures, synchronization and integration fragility.

## L3 — Data / Information
Patient/material identity, lineage, provenance, data quality, semantics, units, timestamps and master/reference-data inconsistencies.

## L4 — Patient / Material / Product Domain
Patient ↔ collection ↔ material ↔ container ↔ shipment ↔ batch ↔ QC ↔ released product ↔ infusion relationships.

## L5 — Treatment Journey / Domain Behavior
Eligibility, apheresis, manufacturing slot, manufacturing, QC/QA release, logistics, conditioning and infusion dependencies.

## L6 — Process / Operations
Manual handoffs, exceptions, approvals, spreadsheets, email workflows, reconciliation, workarounds and shadow processes.

## L7 — Enterprise
CRM + ERP + MES + LIMS + QMS + scheduling + clinical systems + logistics + finance/reimbursement.

## L8 — External Healthcare Ecosystem
Treatment centers + CDMOs + laboratories + couriers + suppliers + payers + regulators + countries.

## L9 — Resilience / Continuity
Manufacturing disruption, failed collection, QC delays, logistics disruption, site outages, alternate capacity, degraded operations and recovery.

## L10 — Decision Intelligence Gaps
Poor forecasting, fragmented prioritization, uncertainty, weak exception intelligence, inadequate optimization and limited causal/contextual reasoning.

## L11 — Assurance / Governance / Authority
Patient safety, GxP, privacy, chain-of-identity, chain-of-custody, decision authority, HITL, validation, TEVV, auditability and regulatory assurance.

## Eight forensic lenses
For every layer ask: **imperfection, inconsistency, friction, complexity, volatility, uncertainty, hidden dependency, unknown unknown**.
