# Stage 4 - Intended Purpose and Applicability Screen

**Status:** Preliminary screen; Legal, Regulatory, Privacy and Quality confirmation required  
**Assessment date:** 2026-09-14  
**Nature:** Architecture/risk analysis, not legal advice or a compliance determination

## 1. Intended purpose

The capstone is a local, synthetic, non-production proof of concept for coordinating an individualized Cell and Gene Therapy patient-to-batch journey. It reconstructs evidence from multiple simulated sources, applies deterministic rules, manages exceptions and presents bounded AI-generated summaries or recommendations to authenticated operational users.

The capstone is intended to:

- expose source disagreement, missing evidence and uncertainty;
- calculate evidence-bearing operational readiness without treating manufacturing completion as Quality release;
- coordinate idempotent, reversible cross-system work;
- support human investigation and planning with grounded recommendations; and
- preserve decision authority, provenance and audit evidence.

It is not intended to:

- diagnose, treat or recommend clinical care;
- autonomously identify a patient, establish Chain of Identity/Custody, close a deviation, disposition product or release a batch;
- replace a clinical, manufacturing or Quality professional;
- serve as a validated GxP production record or electronic-signature system;
- determine eligibility for healthcare/public benefits, perform insurance risk/pricing, or perform emergency triage;
- use real personal or patient data in the capstone; or
- be placed on the market or put into service through this academic deliverable.

Any material change to intended purpose, users, data, geography, authority or integration invalidates this screen and requires reassessment.

## 2. Known deployment facts and open context

| Factor | Current capstone fact | Production question |
|---|---|---|
| Data | Repository states all records are fictional and synthetic | Will identifiable patient, employee or supplier data be processed? |
| Environment | Local POC and simulation | Which countries, legal entities and regulated facilities will deploy it? |
| Records | Demonstration evidence only | Which records are required by applicable predicate rules and relied upon electronically? |
| Signatures | No validated electronic signature claim | Will an electronic approval be intended as a handwritten-signature equivalent? |
| AI | Optional bounded assistant; disabled by default | Which model/provider, processing geography and contractual terms apply? |
| Decision role | Read, extract, summarize, explain and recommend | Could users rely on an output for a safety, quality, clinical or access decision? |
| Product status | Not marketed or deployed | Is it a regulated product, or a safety component of one, in any jurisdiction? |

## 3. Applicability screen

| Regime/control family | POC screen | Basis | Production trigger or unresolved question | Required owner/action |
|---|---|---|---|---|
| 21 CFR Part 11 | **Not presently asserted in scope** | The POC is synthetic and is not a regulated production record/signature system | Electronic records maintained or relied upon under FDA predicate rules, or electronic signatures used as handwritten equivalents | Regulatory/Quality must map each record to its predicate rule and reliance model |
| FDA predicate/GxP requirements | **Undetermined** | No real sponsor, manufacturer, facility, process or regulated use is supplied | Use in manufacture, Quality, clinical investigation or another FDA-regulated activity | Regulatory/Quality must identify the regulated activity and governing predicates |
| EU AI Act - territorial/application scope | **Undetermined for production** | No EU provider, deployer, market placement or affected-person context is supplied | EU market/deployer/use or outputs used in the Union, subject to the Regulation's scope | Legal must confirm operator role, geography and effective obligations at deployment date |
| EU AI Act - prohibited practices | **No intended prohibited practice identified** | Intended use excludes manipulation, exploitation, social scoring, biometric categorization/emotion inference and prohibited identification uses | Any new profiling, biometric, manipulative or deceptive feature | Product/Security/Legal prohibit by requirement and reassess changes |
| EU AI Act - high-risk classification | **Preliminary: not demonstrated high-risk; classification open** | The bounded assistant is designed as a preparatory/recommendation function and is not intended as an Annex I safety component or listed Annex III decision system | Safety component of a regulated product requiring third-party conformity; public-benefit healthcare eligibility; health-insurance risk/pricing; emergency triage; profiling; or material influence over health/safety/fundamental-rights decisions | Legal/Regulatory must document Article 6/Annex I/III assessment for the final intended purpose |
| EU AI Act - transparency/AI literacy | **Design-relevant if deployed in EU** | The interface may directly expose AI-generated material to operational users | AI interaction or generated content within applicable EU use | Disclose AI involvement; train users; retain model/prompt/version evidence |
| GDPR | **Not triggered by the stated synthetic dataset; production applicability open** | The package says people and identifiers are fictional | Processing personal data in EU scope, especially health/special-category data | Privacy must establish controller/processor roles, legal basis, Article 9 condition, DPIA need, minimization and transfer controls |
| HIPAA Privacy/Security/Breach Rules | **Not triggered by the stated synthetic dataset; production applicability open** | No real PHI/ePHI and no covered-entity/business-associate status is established | A covered entity or business associate creates, receives, maintains or transmits PHI/ePHI | Privacy/Security must confirm entity role, BAA chain and safeguards |
| ISO/IEC 42001:2023 | **Voluntary management-system reference** | Relevant to AI governance and continual improvement; no certification claimed | Organizational adoption, customer requirement or certification scope | AIMS owner maps lifecycle evidence; independent certification is out of capstone scope |
| ISO/IEC 42005:2025 | **Applicable good-practice reference** | Designed for AI system impact assessment throughout the lifecycle | Any AI-assisted variant proceeds beyond option evaluation | Stage 7 creates and maintains an impact assessment |
| Records retention/e-discovery | **Undetermined** | The synthetic licence does not define organizational retention | Regulated records, contracts, legal holds or operational incident evidence | Legal/Records owner defines schedule, holds and disposition |
| Licensing/IP | **Restricted to evidenced educational use pending review** | Supplied licence describes a synthetic educational/engineering asset but does not establish rights for every future dependency/model | Redistribution, commercialization, external datasets/models or generated artifacts | Legal/Supplier owner records licences, terms, attribution and usage restrictions |

## 4. 21 CFR Part 11 design implication

FDA guidance says the Part 11 scope depends on whether electronic records/signatures are required by predicate rules and relied on electronically. Therefore, the architecture must not declare “Part 11 compliant.” It will instead prepare control capabilities that would support later validation if the real use is confirmed:

- unique authenticated identities and authorized access;
- authority and operational checks;
- signature meaning and linkage to the signed record;
- immutable before/after audit evidence and clear timestamps;
- record integrity, availability, retention and export;
- versioned procedures, training and change control; and
- risk-based validation evidence.

These are requirements candidates, not validated controls.

## 5. EU AI Act classification hypothesis

The final classification depends on intended purpose, product status, users, geography and actual influence on decisions. For this POC:

1. The deterministic orchestrator is ordinary software unless a final feature meets the Regulation's AI-system definition.
2. An LLM evidence assistant is likely an AI system if deployed within scope.
3. No intended feature matches the screened Article 5 prohibited practices.
4. The operational recommendation use case does not obviously match Annex III as currently bounded.
5. Article 6(1) could change the result if the AI becomes a safety component of an Annex I regulated product requiring third-party conformity assessment.
6. A feature that materially determines public healthcare access, health-insurance risk/pricing or emergency patient triage would require a different assessment and is outside scope.
7. Even a non-high-risk conclusion must be documented where Article 6(3)/(4) applies, and transparency, literacy, privacy and other law may still apply.

## 6. Privacy-by-design implications

The POC uses only the provided synthetic records. The production design must assume health data is highly sensitive until Privacy confirms otherwise and must specify:

- data minimization and purpose limitation;
- pseudonymous operational keys and controlled re-identification;
- least-privilege access by patient, site, function and case;
- field-level provenance and access logging;
- protected logs, prompts, traces and evaluation datasets;
- provider data-use, retention, training and transfer restrictions;
- DLP/redaction before any external model call;
- access, correction, retention, deletion/hold and breach workflows; and
- an AI-disabled path that prevents unnecessary external processing.

## 7. Official reference set

- [FDA Part 11: Electronic Records; Electronic Signatures - Scope and Application](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)
- [FDA: Electronic Systems, Electronic Records, and Electronic Signatures in Clinical Investigations](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-systems-electronic-records-and-electronic-signatures-clinical-investigations-questions)
- [EU Regulation 2024/1689 (Artificial Intelligence Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [European Commission AI Act overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [EU General Data Protection Regulation](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [HHS summary of the HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/42001)
- [ISO/IEC 42005:2025](https://www.iso.org/standard/42005)

## 8. Mandatory expert decisions before a real pilot

1. Regulatory determines the governed activity and applicable predicate rules.
2. Quality determines which records/signatures are relied upon and the validation category.
3. Legal determines geography, EU AI Act operator/classification and contract/licence obligations.
4. Privacy determines personal-data roles, legal basis, special-category condition and DPIA/BAA needs.
5. Security approves identity, access, logging, supplier and data-transfer controls.
6. Product freezes the intended purpose and initiates reassessment for any material change.
