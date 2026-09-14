#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "openai_style_key": re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}
EXCLUDED_PARTS = {".git", ".venv", "__pycache__"}


def main() -> None:
    findings = []
    scanned = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or EXCLUDED_PARTS & set(path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append({"path": path.relative_to(ROOT).as_posix(), "pattern": name})
    runtime_databases = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*.db") if ".git" not in path.parts and "source_baseline" not in path.parts]
    report = {
        "scope": "pattern-based academic repository scan; not a production secret scanner",
        "text_files_scanned": scanned,
        "credential_pattern_findings": findings,
        "runtime_databases_outside_source_baseline": runtime_databases,
        "live_model_credentials_expected": False,
        "pass": not findings and not runtime_databases,
    }
    output = ROOT / "docs/stages/stage_21/retirement_scan.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
