# Stage 12 - Security, Privacy and Guardrail Controls

| Control | POC implementation | Production gap |
|---|---|---|
| Authentication | Explicit demo principal header/config; deny absent principal for mutations | Enterprise IdP/MFA/session assurance |
| Authorization | Server-side role/scope map; exact action checks | Formal RBAC/ABAC governance and recertification |
| Least privilege | Assistant read/recommend only; no mutating tool | Infrastructure/service identities |
| Data minimization | Synthetic scoped fields; no whole-repository prompt | Approved PHI field/purpose mapping |
| Encryption | Local development filesystem/process boundary | Managed TLS/KMS/rotation/HSM requirements |
| Audit | Append-only logical ledger with hash chain | Validated immutable/WORM storage and retention |
| Input validation | Typed domain checks, canonical JSON digests | Gateway/WAF and full schema fuzzing |
| Output guardrail | Allowlisted assistant schema/evidence; reject extra authority fields | Live-model red team and continuous monitoring |
| DLP | Synthetic-only and no external provider | Enterprise DLP/redaction/incident process |
| Availability | AI-off mode, explicit unknown/recovery | HA, DR, dependency SLOs |
| Secure delivery | Tests, dependency manifest, non-root image | Signed provenance, SAST/DAST/SCA infrastructure |

No secret is required for the shipped POC. `.env` is ignored. A future provider credential must be injected at runtime and never stored in source, fixtures, reports or audit payloads.
