# Stage 12 - Security and AI Threat Model

**Scope:** Local synthetic POC. Production assessment remains required.

## Trust boundaries

1. User/browser to API.
2. API to application/domain services.
3. Application to SQLite and evidence files.
4. Application to simulated external adapters.
5. Deterministic context to optional assistant/model port.
6. Build environment to dependency/container supply chain.

| ID | Threat | Harm | Controls | Verification |
|---|---|---|---|---|
| T01 | Spoofed role or body-supplied authority | Unauthorized identity/release/command | Server-side principal/role/scope; deny by default | EXT-ID-002; EXT-AUTH-001..003 |
| T02 | Approval payload swapped after review | Wrong consequential action | Digest-bind proposal/evidence/payload | EXT-ID-003; EXT-AUTH-003 |
| T03 | Event/audit tampering | Untrustworthy history | Append-only API, digest chain, integrity check | EXT-SEC-002 |
| T04 | Cross-patient IDOR | Sensitive-data disclosure | Scope checks on every object lookup | EXT-SEC-001 |
| T05 | Prompt injection in notes/SOPs | Policy bypass/tool misuse | Untrusted-content boundary; no assistant write tools | EVAL-006; EXT-AI-001 |
| T06 | Model hallucination/omission | Misleading recommendation | Evidence allowlist, schema, uncertainty, deterministic view | EXT-AI-003; EXT-AI-006 |
| T07 | Sensitive prompt/output/log leakage | Privacy harm | Synthetic-only, minimization, redaction, no external model | EXT-AI-002 |
| T08 | Denial through model outage/loop | Workflow unavailable | AI-off fallback, timeout, one call, no loop | EXT-AI-005; EXT-AI-007 |
| T09 | Retry/replay attack | Duplicate external effect | Semantic idempotency, reconciliation, authorization | INJ-006; EXT-CMD-001..004 |
| T10 | Malicious/corrupt source record | Wrong canonical state | Source assertions, validation, conflict/unknown | EVAL-002..003 |
| T11 | Dependency/container compromise | Code execution/data loss | Pinned minimal dependencies, hashes/CI scan plan, non-root image | SBOM/release checks |
| T12 | Secrets committed or logged | Credential disclosure | No live credential, env-only future secret, secret scan | Repository scan |

## Abuse cases

The system must resist a courier note claiming release authority, a request body claiming `QualityApprover`, replay with changed payload, cross-scope object IDs, malformed AI JSON, evidence references not in context, unknown external outcomes and altered audit rows. All consequential denials are auditable.

## Residual position

The threat controls are implemented and internally tested only for the local POC after Stage 14. They do not establish production penetration-test, privacy, network, IAM, cryptographic, supplier or facility assurance.
