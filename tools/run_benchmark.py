#!/usr/bin/env python3
from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fde_capstone.application import CapstoneApplication
from fde_capstone.model import Outcome, Principal


def main() -> None:
    app = CapstoneApplication(":memory:")
    viewer = Principal("benchmark", frozenset({"VIEWER"}), frozenset({"*"}))
    mapping = {"identity": "EV-ID", "consent": "EV-CONSENT", "authorization": "EV-AUTH", "site": "EV-SITE"}
    for item in mapping.values():
        app.evidence.register(item, "BENCH", f"bench://{item}", {"id": item}, "2026-01-01T00:00:00+00:00", "2026-01-01T00:00:00+00:00")
    prereqs = {name: (Outcome.SATISFIED, [item]) for name, item in mapping.items()}
    samples = []
    for _ in range(5000):
        start = time.perf_counter()
        app.readiness.assess(viewer, "P-1", "PRE_COLLECTION", prereqs)
        samples.append((time.perf_counter() - start) * 1000)
    report = {
        "scope": "single-process local synthetic micro-benchmark; not production load test",
        "iterations": len(samples),
        "median_ms": round(statistics.median(samples), 4),
        "p95_ms": round(statistics.quantiles(samples, n=100)[94], 4),
        "p99_ms": round(statistics.quantiles(samples, n=100)[98], 4),
        "threshold_p95_ms": 250,
        "pass": statistics.quantiles(samples, n=100)[94] <= 250,
    }
    app.close()
    output = ROOT / "docs/stages/stage_15/performance_results.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
