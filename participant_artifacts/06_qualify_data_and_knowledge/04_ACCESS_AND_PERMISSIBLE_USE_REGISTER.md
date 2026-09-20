# Stage 6 - Access, Classification and Permissible-Use Register

**Status:** Capstone policy proposal; Privacy, Legal, Security and data-owner approval pending  
**Last updated:** 2026-09-14

## 1. Current data classification

The source package states that all people, organizations, identifiers, products, events and operational records are fictional and synthetic. For the capstone, the data is classified as:

`SYNTHETIC-SENSITIVE-SIMULATION`

It is not real PHI, but it intentionally resembles high-sensitivity patient/manufacturing/Quality data. Controls should demonstrate the production pattern without claiming that the current files create HIPAA/GDPR compliance obligations.

## 2. Permissible-use register

| Use | POC decision | Conditions |
|---|---|---|
| Local forensic analysis and profiling | Allowed | Preserve immutable baseline and hashes |
| Deterministic development/testing | Allowed | Use working copies/fixtures; do not rewrite baseline |
| Evaluation and red-team testing | Allowed | Retain synthetic classification and evidence lineage |
| Local/mock AI evaluation | Allowed | No claim of model quality beyond measured cases |
| External model/API use | Denied by default | Requires explicit provider, data-use, retention, transfer, security, cost and credential approval; synthetic minimum data only |
| Training/fine-tuning a model | Not approved | Separate purpose, licence, data and impact assessment required |
| Public redistribution | Not approved | Supplied licence/third-party rights require Legal confirmation |
| Production decision making | Prohibited | Dataset is synthetic and system is not validated/deployed |
| Clinical, identity, COI/COC or Quality ground truth | Prohibited claim | No authorized ground truth is supplied |
| Production performance/compliance/savings claim | Prohibited claim | Requires real controlled evidence and approval |

## 3. Role-to-data access hypothesis

| Role | Minimum read scope | Write/decision scope | Restrictions |
|---|---|---|---|
| Clinical Operations | Assigned journey, consent/site/clinical readiness and relevant product evidence | Authorized clinical/identity workflow only | No Quality release or global data export |
| Identity/Data Steward | Minimum identity assertions and conflict evidence | Resolution proposal/application after required approval | No clinical/Quality decision |
| Manufacturing Planner | Pseudonymous journey/slot/logistics constraints | Approved reservation commands | No unnecessary demographics/clinical detail |
| Logistics Coordinator | Shipment/custody route and minimum pseudonymous linkage | Shipment/case workflow | No broad patient identity or Quality release authority |
| Quality/QP | Batch, QC, deviation, thermal, lineage and required patient-specific evidence | Disposition/release/closure per policy | No role self-assertion; signature/SoD required |
| Site Coordinator | Assigned center/journey readiness | Site/receipt acknowledgements under policy | Center/site scope only |
| Security/Privacy | Access/audit/security metadata; controlled content access for investigation | Security/privacy control decisions | Least privilege and break-glass audit |
| Platform/SRE | Service/trace metadata with protected content redacted | Operational recovery | No business approval; production content restricted |
| AI service identity | Minimum retrieved evidence for one authorized task | None; recommendation record only | No consequential adapter credential or unrestricted memory |
| Evaluation runner | Synthetic golden/failure set | Test output only | Isolated from production data/credentials |

## 4. Purpose and field minimization

| Workflow | Needed identity exposure | Unnecessary by default |
|---|---|---|
| Capacity planning | Pseudonymous journey/product/site/timing/constraints | Name, DOB, MRN, detailed clinical notes |
| Logistics | Shipment/COI pseudonym, origin/destination, custody/condition | Full identity and unrelated clinical/payer data |
| Quality release support | Batch/product/COI, QC/deviation/thermal and authorized linkage evidence | Commercial identity fields not required for review |
| Identity reconciliation | Minimum disputed/corroborating identity attributes | Full journey evidence unrelated to resolution |
| Executive analytics | Aggregated/de-identified KPIs | Row-level identity or unredacted notes |
| AI summary | Minimum task-specific evidence and references | Raw export dump, secrets, credentials, unrestricted logs |

## 5. Required access controls

- Authenticate users/services through a trusted identity provider.
- Derive role, assignment, purpose and resource scope server-side.
- Enforce patient/site/function/record-level authorization.
- Separate read, recommend, approve, execute and administer permissions.
- Redact/minimize prompts, traces, logs, exports and evaluation artifacts.
- Use short-lived least-privilege service credentials and protected secret storage.
- Record allowed and denied access with purpose and trace correlation.
- Require break-glass reason, time limit, alert and retrospective review.
- Disable external AI by default and retain the deterministic workflow.
- Test prompt injection, cross-tenant/resource leakage and role spoofing.

## 6. Lifecycle/retention questions

The challenge does not supply retention, legal hold, subject-right, correction or deletion schedules. Stage 9/12 must specify separately for:

- immutable source evidence;
- canonical assertions/events;
- approvals/signatures/audit;
- operational cases and attachments;
- prompts, completions, tool traces and evaluation data;
- model/prompt/policy versions;
- backups and exports; and
- derived analytics and aggregate reports.

No “right to delete” implementation may silently destroy records subject to legal/regulatory hold; no retention requirement may be invented without owner approval.

## 7. Production privacy gate

Before real data is introduced, Privacy/Legal must document jurisdiction, controller/processor or covered-entity/business-associate roles, purpose/legal basis, special-category condition, minimization, DPIA/BAA/contract needs, residency/transfers, provider training/retention terms, data-subject/patient rights, breach response and disposition. Until then, production data use is no-go.
