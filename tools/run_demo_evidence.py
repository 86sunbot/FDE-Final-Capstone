#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fde_capstone.demo import run_demo


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="fde-demo-") as temp:
        directory = Path(temp)
        report = {
            "ai_off": run_demo(directory / "ai-off.db", "off"),
            "bounded_fake": run_demo(directory / "fake.db", "fake"),
            "limitations": ["synthetic data", "simulated authorities/adapters", "fake assistant is not live-model evidence"]
        }
    output = ROOT / "docs/stages/stage_14/integrated_demo_results.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ai_off_audit": report["ai_off"]["audit_chain_valid"], "fake_audit": report["bounded_fake"]["audit_chain_valid"]}, indent=2))


if __name__ == "__main__":
    main()
