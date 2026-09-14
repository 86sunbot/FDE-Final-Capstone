# FDE Final Capstone

This repository is the completed **synthetic academic** Cell and Gene Therapy patient-to-batch orchestration capstone. It follows the 21-stage AI FDE operating model from problem discovery through engineering, assurance, simulated operation, lifecycle decision and retirement.

## What it solves

The inherited environment had conflicting patient evidence, unsafe readiness/release shortcuts, weak retry handling and fragmented exception work. This solution provides one evidence-driven orchestration layer with:

- source-specific assertions and bitemporal history;
- explicit satisfied/not-satisfied/unknown outcomes;
- human-authorized identity and Quality decisions;
- safe idempotent commands and reconciliation;
- owned exceptions and tamper-evident audit;
- three integrated POCs;
- one optional recommendation-only assistant, disabled by default.

## Important boundary

This is not a production, clinical, regulatory or validated system. It uses synthetic data and simulated authorities/integrations. No live AI model is included. The final lifecycle decision is **restrict and change**: accept the academic POC, keep AI off and do not pilot with real data until the seven CAPAs in Stage 20 are closed.

## Results

- 73 automated tests passed.
- 57 evaluation cases executed: 55 internal structural passes, 0 failures and 2 human-study cases inconclusive.
- 20/20 simulated shadow comparisons matched.
- 10/10 simulated canary journeys succeeded.
- Backup/restore and AI-off rollback passed locally.
- Original ZIP and all 132 extracted evidence files remained unchanged.

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev,api]'
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m fde_capstone.cli demo --db runtime/demo.db
PYTHONPATH=src .venv/bin/python -m fde_capstone.cli evaluate --db runtime/eval.db --output reports/evaluation.json
```

Delete `runtime/` after the demo; it contains disposable synthetic state.

Start with [FINAL_CAPSTONE_REPORT.md](FINAL_CAPSTONE_REPORT.md), then use [CAPSTONE_PROGRESS_TRACKER.md](CAPSTONE_PROGRESS_TRACKER.md) and [ARTIFACT_INDEX.md](ARTIFACT_INDEX.md).
