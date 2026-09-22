#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fde_capstone.adapters.assistant_fake import FailingAssistantFake
from fde_capstone.application import CapstoneApplication
from fde_capstone.model import Principal
from fde_capstone.services.assistant import AssistantGateway


def main() -> None:
    app = CapstoneApplication(":memory:", ai_mode="fake")
    planner = Principal("monitor-planner", frozenset({"PLANNER"}), frozenset({"*"}))
    viewer = Principal("monitor-viewer", frozenset({"VIEWER"}), frozenset({"*"}))
    for index in range(10):
        app.commands.reserve_slot(planner, f"KEY-{index}", f"P-{index}", f"S-{index}")
    for index in range(3):
        result = app.commands.reserve_slot(planner, f"UNK-{index}", f"PU-{index}", f"SU-{index}", "timeout_after_success")
        app.commands.reconcile(planner, result["command_id"])
    app.commands.reserve_slot(planner, "CONFLICT", "PC", "S1")
    app.commands.reserve_slot(planner, "CONFLICT", "PC", "S2")
    context = {"state": "QUALITY_REVIEW", "blockers": [], "unknowns": ["QMS_OUTAGE"], "available_evidence": ["EV-REFERENCE"]}
    app.assistant.recommend("B-1", context)
    AssistantGateway(app.db, FailingAssistantFake()).recommend("B-1", context)
    authorization_denied = False
    try:
        app.commands.reserve_slot(viewer, "DENIED", "P-DENIED", "S-DENIED")
    except PermissionError:
        authorization_denied = True
    metrics = app.db.metrics()
    report = {
        "scope": "synthetic operational monitoring simulation",
        "metrics": metrics,
        "audit_chain_valid": app.db.verify_audit_chain(),
        "authorization_denial_observed": authorization_denied,
        "alerts": [
            {"alert": "UNKNOWN_OUTCOME_RATE", "observed": metrics.get("unknown_outcomes", {}).get("count", 0), "status": "EXERCISED"},
            {"alert": "IDEMPOTENCY_CONFLICT", "observed": metrics.get("idempotency_conflicts", {}).get("count", 0), "status": "EXERCISED"},
            {"alert": "AI_FALLBACK", "observed": metrics.get("recommendation_fallbacks", {}).get("count", 0), "status": "EXERCISED"},
            {"alert": "AUTHORIZATION_DENIED", "observed": metrics.get("authorization_denied", {}).get("count", 0), "status": "EXERCISED"}
        ],
        "source_drift": {"status": "NOT_OBSERVED_IN_FIXED_FIXTURE", "production_monitor": "REQUIRED"},
        "pass": app.db.verify_audit_chain() and authorization_denied,
    }
    app.close()
    output = ROOT / "docs/stages/stage_18/monitoring_simulation_results.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
