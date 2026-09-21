import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = json.loads((ROOT / "docs/stages/stage_02" / "evidence_inventory.json").read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def test_every_extracted_source_file_matches_frozen_zip_inventory() -> None:
    files = INVENTORY["files"]
    assert len(files) == 132
    expected_paths = {record["relative_path"] for record in files}
    actual_paths = {
        path.relative_to(ROOT / "source_baseline").as_posix()
        for path in (ROOT / "source_baseline").rglob("*")
        if path.is_file()
    }
    assert actual_paths == expected_paths
    for record in files:
        path = ROOT / "source_baseline" / record["relative_path"]
        assert path.is_file(), record["relative_path"]
        assert path.stat().st_size == record["size_bytes"], record["relative_path"]
        assert digest(path) == record["sha256"], record["relative_path"]


def test_frozen_zip_identity_is_the_expected_challenge_baseline() -> None:
    assert INVENTORY["source_zip_sha256"] == "74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979"
    assert INVENTORY["summary"]["internal_manifest_verified"] == 130
    assert INVENTORY["summary"]["internal_manifest_missing"] == []
    assert INVENTORY["summary"]["internal_manifest_mismatched"] == []
