#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fde_capstone.application import CapstoneApplication
from fde_capstone.demo import run_demo


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="fde-recovery-") as temp:
        directory = Path(temp)
        source = directory / "source.db"
        backup = directory / "backup.db"
        run_demo(source)
        app = CapstoneApplication(source)
        before = app.db.state_digest()
        start = time.perf_counter()
        app.db.backup(backup)
        app.close()
        restored = CapstoneApplication(backup)
        after = restored.db.state_digest()
        audit_valid = restored.db.verify_audit_chain()
        restored.close()
        seconds = time.perf_counter() - start
    report = {
        "scope": "local temporary SQLite synthetic recovery drill",
        "state_digest_before": before,
        "state_digest_after": after,
        "digest_match": before == after,
        "audit_chain_valid": audit_valid,
        "recovery_seconds": round(seconds, 6),
        "rto_target_seconds": 60,
        "rpo_target": "zero committed local transactions at backup boundary",
        "pass": before == after and audit_valid and seconds <= 60,
        "production_claim": False
    }
    output = ROOT / "stage_16/recovery_drill_results.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
