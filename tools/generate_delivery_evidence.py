#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(paths: list[Path]) -> tuple[str, list[dict]]:
    records = []
    for base in paths:
        for path in sorted(
            item
            for item in base.rglob("*")
            if item.is_file()
            and "__pycache__" not in item.parts
            and not any(part.endswith(".egg-info") for part in item.parts)
        ):
            records.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "size_bytes": path.stat().st_size})
    value = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return value, records


def version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def main() -> None:
    generated_at = datetime.now(UTC).isoformat()
    source_digest, source_files = tree_digest([ROOT / "src"])
    contract_digest, contract_files = tree_digest([ROOT / "docs/stages/stage_09/contracts"])
    evaluation_catalog = ROOT / "docs/stages/stage_07/evaluation_catalog.json"
    requirements = ROOT / "requirements/requirements.csv"
    sbom = {
        "format": "academic-capstone-sbom-v1",
        "generated_at": generated_at,
        "runtime": {"python": platform.python_version(), "sqlite": __import__("sqlite3").sqlite_version, "platform": platform.platform()},
        "application": {"name": "fde-final-capstone", "version": "1.2.0", "source_tree_sha256": source_digest},
        "dependencies": [
            {"name": "fastapi", "version": version("fastapi"), "scope": "optional API"},
            {"name": "uvicorn", "version": version("uvicorn"), "scope": "optional API server"},
            {"name": "httpx", "version": version("httpx"), "scope": "API test client"},
            {"name": "mypy", "version": version("mypy"), "scope": "static type analysis"},
            {"name": "pytest", "version": version("pytest"), "scope": "test"},
            {"name": "pytest-cov", "version": version("pytest-cov"), "scope": "test coverage"},
            {"name": "ruff", "version": version("ruff"), "scope": "lint"},
        ],
        "limitations": "Not a signed CycloneDX/SPDX production attestation."
    }
    aibom = {
        "format": "academic-capstone-aibom-v1",
        "generated_at": generated_at,
        "live_model_provider": None,
        "live_model": None,
        "training_or_fine_tuning": None,
        "embedding_or_vector_store": None,
        "test_adapter": "DeterministicAssistantFake v1",
        "ai_modes": ["off", "fake"],
        "default_mode": "off",
        "tools": ["read scoped deterministic context"],
        "consequential_tools": [],
        "output_contract_sha256": sha(ROOT / "docs/stages/stage_09/contracts/recommendation.schema.json"),
        "limitations": "No live-model quality, safety, privacy, latency or cost evidence."
    }
    manifest = {
        "format": "academic-capstone-release-manifest-v1",
        "version": "1.2.0",
        "generated_at": generated_at,
        "scope": "synthetic local academic POC",
        "source_tree_sha256": source_digest,
        "contract_tree_sha256": contract_digest,
        "evaluation_catalog_sha256": sha(evaluation_catalog),
        "requirements_sha256": sha(requirements),
        "schema_version": "1",
        "ai_default": "off",
        "original_zip_sha256": "74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979",
        "source_files": source_files,
        "contract_files": contract_files,
        "known_limits": ["synthetic data", "simulated external systems and authorities", "no live model", "no independent assurance", "not production validated"]
    }
    for path, payload in [
        (ROOT / "docs/stages/stage_14/SBOM.json", sbom),
        (ROOT / "docs/stages/stage_14/AIBOM.json", aibom),
        (ROOT / "docs/stages/stage_14/release_manifest.json", manifest),
    ]:
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_tree_sha256": source_digest, "contract_tree_sha256": contract_digest, "source_files": len(source_files), "contract_files": len(contract_files)}, indent=2))


if __name__ == "__main__":
    main()
