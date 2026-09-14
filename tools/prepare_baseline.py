#!/usr/bin/env python3
"""Verify, inventory, and safely extract the immutable challenge package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZipInfo


EXPECTED_ZIP_SHA256 = "74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979"
PACKAGE_ROOT = "AI_FDE_CGT_Patient_to_Batch_Orchestration_v2/"
CHECKSUM_ENTRY = PACKAGE_ROOT + "checksums.sha256"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def classify(relative_path: str) -> str:
    path = PurePosixPath(relative_path)
    if relative_path in {"README.md", "AGENTS.md", "VERIFICATION.md"}:
        return "governance_context"
    if path.parts and path.parts[0] == "participant":
        return "challenge_requirement"
    if path.parts and path.parts[0] == "data":
        return "structured_evidence"
    if path.parts and path.parts[0] == "shadow_ops":
        return "shadow_operations_evidence"
    if path.parts and path.parts[0] == "contracts":
        return "interface_evidence"
    if path.parts and path.parts[0] == "docs":
        return "documentation_or_rule_evidence"
    if path.parts and path.parts[0] == "evals":
        return "evaluation_evidence"
    if path.parts and path.parts[0] == "scenarios":
        return "failure_scenario_evidence"
    if path.parts and path.parts[0] in {"src", "tests", "scripts", "tools"}:
        return "executable_evidence"
    return "repository_support"


def safe_member(info: ZipInfo) -> bool:
    path = PurePosixPath(info.filename)
    return not path.is_absolute() and ".." not in path.parts


def load_internal_checksums(archive: ZipFile) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in archive.read(CHECKSUM_ENTRY).decode("utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative_path = line.split(maxsplit=1)
        rows[relative_path.lstrip("* ")] = expected
    return rows


def build_inventory(archive: ZipFile, internal: dict[str, str]) -> tuple[list[dict[str, object]], dict[str, object]]:
    inventory: list[dict[str, object]] = []
    listed_ok = 0
    listed_missing: list[str] = []
    listed_mismatch: list[str] = []

    names = set(archive.namelist())
    for relative_path, expected in internal.items():
        entry = PACKAGE_ROOT + relative_path
        if entry not in names:
            listed_missing.append(relative_path)
            continue
        actual = sha256_bytes(archive.read(entry))
        if actual == expected:
            listed_ok += 1
        else:
            listed_mismatch.append(relative_path)

    for info in sorted(archive.infolist(), key=lambda item: item.filename):
        if not safe_member(info):
            raise ValueError(f"Unsafe ZIP entry: {info.filename}")
        if info.is_dir():
            continue
        relative_path = info.filename.removeprefix(PACKAGE_ROOT)
        content = archive.read(info.filename)
        actual = sha256_bytes(content)
        expected = internal.get(relative_path)
        inventory.append(
            {
                "entry_path": info.filename,
                "relative_path": relative_path,
                "classification": classify(relative_path),
                "size_bytes": info.file_size,
                "compressed_bytes": info.compress_size,
                "sha256": actual,
                "listed_in_internal_manifest": expected is not None,
                "internal_manifest_match": None if expected is None else actual == expected,
            }
        )

    summary = {
        "zip_entries_total": len(archive.infolist()),
        "files_total": len(inventory),
        "directories_total": sum(1 for item in archive.infolist() if item.is_dir()),
        "internal_manifest_listed": len(internal),
        "internal_manifest_verified": listed_ok,
        "internal_manifest_missing": listed_missing,
        "internal_manifest_mismatched": listed_mismatch,
        "classification_counts": {},
    }
    counts: dict[str, int] = {}
    for item in inventory:
        key = str(item["classification"])
        counts[key] = counts.get(key, 0) + 1
    summary["classification_counts"] = counts
    return inventory, summary


def write_outputs(
    zip_path: Path,
    inventory: list[dict[str, object]],
    summary: dict[str, object],
    csv_path: Path,
    json_path: Path,
) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(inventory[0].keys()) if inventory else []
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(inventory)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_zip": str(zip_path),
        "source_zip_size_bytes": zip_path.stat().st_size,
        "source_zip_sha256": sha256_file(zip_path),
        "expected_zip_sha256": EXPECTED_ZIP_SHA256,
        "summary": summary,
        "files": inventory,
    }
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def safe_extract(archive: ZipFile, output_root: Path) -> Path:
    if output_root.exists():
        raise FileExistsError(f"Refusing to overwrite existing baseline: {output_root}")
    output_root.parent.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix="baseline.", dir=output_root.parent))
    try:
        for info in archive.infolist():
            if not safe_member(info):
                raise ValueError(f"Unsafe ZIP entry: {info.filename}")
            archive.extract(info, temp_root)
        extracted = temp_root / PACKAGE_ROOT.rstrip("/")
        if not extracted.is_dir():
            raise ValueError("Expected package root was not extracted")
        extracted.rename(output_root)
        temp_root.rmdir()
    except Exception:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise

    for path in output_root.rglob("*"):
        if path.is_file():
            path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        elif path.is_dir():
            path.chmod(stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    output_root.chmod(stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    return output_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--inventory-csv", required=True, type=Path)
    parser.add_argument("--inventory-json", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    zip_path = args.zip.resolve()
    actual_zip_sha256 = sha256_file(zip_path)
    if actual_zip_sha256 != EXPECTED_ZIP_SHA256:
        print(
            f"ZIP integrity failure: expected {EXPECTED_ZIP_SHA256}, got {actual_zip_sha256}",
            file=sys.stderr,
        )
        return 2

    with ZipFile(zip_path) as archive:
        if archive.testzip() is not None:
            print("ZIP CRC validation failed", file=sys.stderr)
            return 3
        internal = load_internal_checksums(archive)
        inventory, summary = build_inventory(archive, internal)
        if summary["internal_manifest_missing"] or summary["internal_manifest_mismatched"]:
            print("Internal checksum validation failed", file=sys.stderr)
            return 4
        write_outputs(zip_path, inventory, summary, args.inventory_csv, args.inventory_json)
        safe_extract(archive, args.output)

    print(json.dumps({"status": "PASS", "baseline": str(args.output), **summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
