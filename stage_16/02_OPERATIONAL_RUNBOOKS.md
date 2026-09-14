# Stage 16 - Operational Runbooks

## RB-01 Start and verify

1. Confirm Python version and release-manifest digests.
2. Ensure `AI_MODE=off` unless running the labelled fake-adapter demonstration.
3. Initialize a disposable database with `fde-capstone init`.
4. Run health, audit verification and one read-only deterministic query.
5. Do not proceed if evidence/catalog/source digests differ.

## RB-02 Unknown external command outcome

1. Stop automatic retry.
2. Locate command by ID, idempotency key and correlation ID.
3. Query the simulated/external provider for the exact payload digest.
4. Record effect found, no effect or partial effect.
5. Move to success, explicitly authorized retry, or compensation; retain all attempts.

## RB-03 QMS or Quality evidence outage

1. Keep release state unknown/awaiting Quality.
2. Do not infer from MES, ERP, QC or model text.
3. Open/assign a P0 case and show last evidence timestamp.
4. Restore source and re-run packet; require authorized review.

## RB-04 Model failure or unsafe output

1. Reject invalid output and return deterministic view.
2. Set AI off; no workflow restart is required.
3. Capture model/version, validation reason and correlation without sensitive raw data.
4. Re-enable only after affected evaluation cases pass.

## RB-05 Audit integrity failure

1. Disable mutations and preserve database/image/log copies.
2. Verify manifest, filesystem and audit hashes.
3. Determine first failing record and affected decisions.
4. Escalate; do not repair history in place.

## RB-06 Backup/restore

1. Quiesce or use a consistent database backup boundary.
2. Create backup and record source state digest.
3. Open restored database, migrate if approved, compare state digest and verify audit chain.
4. Record RTO/RPO and exceptions before returning to service.

## RB-07 Rollback

First disable AI. If deterministic release is defective, stop mutations, preserve evidence, restore the last verified database/release and replay only verified events. Confirm no command remained `OUTCOME_UNKNOWN` without owner.
