# Stage 10 - AI Context and Output Design

The assistant receives only the minimum deterministic case summary, explicit blockers/conflicts, available evidence IDs and allowed non-consequential actions. Documents are marked untrusted data. System policy and authority are not retrieved from free text.

The output contract permits only `summary`, `evidence_refs`, `uncertainty` and `next_actions`. Unknown evidence IDs, extra authority fields, invalid shape, timeout or exception cause rejection and deterministic fallback. Raw model text never enters a canonical event payload.

The assistant has no write tools. A later human may independently submit an authenticated command through the normal service after reviewing deterministic evidence; that command is not attributed to the model. Prompts, outputs, model/version, token counts, latency and validation result are traced without storing sensitive raw content by default.

Model quality is not claimed in this repository because no live provider is selected. The fake adapter demonstrates the architectural boundary and permits repeatable adversarial tests.
