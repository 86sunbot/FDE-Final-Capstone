# FDE Final Capstone

This repository is the completed **synthetic academic** Cell and Gene Therapy patient-to-batch orchestration capstone. It follows the 21-stage AI FDE operating model from problem discovery through engineering, assurance, simulated operation, lifecycle decision and retirement.

> **Start here:** [Final report](docs/FINAL_CAPSTONE_REPORT.md) · [Documentation hub](docs/README.md) · [21-stage index](docs/stages/README.md) · [Demo guide](docs/DEMO_GUIDE.md)

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

## Repository layout

| Path | Purpose |
|---|---|
| [`src/fde_capstone`](src/fde_capstone) | Application, services, adapters, API, CLI and browser frontend |
| [`docs`](docs/README.md) | Final report, plan, progress, traceability, demo guide and documentation index |
| [`docs/stages`](docs/stages/README.md) | Every artifact from all 21 FDE operating-model stages |
| [`requirements`](requirements) | Requirements and machine-readable verification/traceability matrices |
| [`evidence`](evidence) | Final independent repository-verification result |
| [`reports`](reports) | Generated JUnit test evidence |
| [`tests`](tests) | Unit, integration, end-to-end, recovery and performance tests |
| [`tools`](tools) | Reproducible evidence, evaluation and verification utilities |
| [`source_baseline`](source_baseline) | Frozen 132-file challenge extraction; do not modify |

## Browser demonstration

On macOS, double-click `START_DEMO.command`, keep its terminal window open, and use the Control Tower page that opens automatically. The browser executes all three POCs against isolated synthetic state; it is not a disconnected mockup.

Alternatively, start it from a terminal:

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev,api]'
FDE_DB=runtime/control-tower.db AI_MODE=off PYTHONPATH=src \
  .venv/bin/python -m uvicorn fde_capstone.api:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000> for the Control Tower and <http://127.0.0.1:8000/docs> for the API. See [docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md) for the five-minute presentation sequence.

## Results

- 77 automated tests passed.
- 57 evaluation cases executed: 55 internal structural passes, 0 failures and 2 human-study cases inconclusive.
- 20/20 simulated shadow comparisons matched.
- 10/10 simulated canary journeys succeeded.
- Backup/restore and AI-off rollback passed locally.
- Original ZIP and all 132 extracted evidence files remained unchanged.

## CLI and evaluation

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev,api]'
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m fde_capstone.cli demo --db runtime/demo.db
PYTHONPATH=src .venv/bin/python -m fde_capstone.cli evaluate --db runtime/eval.db --output reports/evaluation.json
```

Delete `runtime/` after the demo; it contains disposable synthetic state.

## Verification provenance

Local verification directly hashes the original external ZIP when it is available at its recorded path. GitHub Actions intentionally does not receive that external archive; it verifies the recorded ZIP digest plus all 132 committed frozen extraction files against their individual inventory hashes. Generated package metadata such as `*.egg-info` is excluded from the signed application-source digest.

Start with [docs/FINAL_CAPSTONE_REPORT.md](docs/FINAL_CAPSTONE_REPORT.md), then use [docs/CAPSTONE_PROGRESS_TRACKER.md](docs/CAPSTONE_PROGRESS_TRACKER.md) and [docs/ARTIFACT_INDEX.md](docs/ARTIFACT_INDEX.md).
