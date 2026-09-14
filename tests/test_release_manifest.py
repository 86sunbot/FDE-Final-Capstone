import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_release_manifest_binds_source_contracts_catalog_and_requirements():
    manifest = json.loads((ROOT / "docs/stages/stage_14/release_manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "1.1.0"
    assert manifest["ai_default"] == "off"
    assert manifest["original_zip_sha256"] == "74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979"
    assert manifest["evaluation_catalog_sha256"] == sha(ROOT / "docs/stages/stage_07/evaluation_catalog.json")
    assert manifest["requirements_sha256"] == sha(ROOT / "requirements/requirements.csv")
    assert len(manifest["source_files"]) >= 20


def test_aibom_explicitly_has_no_live_model():
    aibom = json.loads((ROOT / "docs/stages/stage_14/AIBOM.json").read_text(encoding="utf-8"))
    assert aibom["live_model_provider"] is None
    assert aibom["live_model"] is None
    assert aibom["default_mode"] == "off"
    assert aibom["consequential_tools"] == []
