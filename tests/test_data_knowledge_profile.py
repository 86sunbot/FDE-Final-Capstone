import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "stage_06" / "data_knowledge_profile.json").read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def test_profile_has_expected_evidence_population() -> None:
    assert PROFILE["summary"] == {
        "csv_datasets": 23,
        "csv_rows": 27507,
        "duplicate_key_groups": 0,
        "relationship_checks": 25,
        "relationship_issues": 188,
        "knowledge_items": 24,
        "event_rows": 6407,
        "event_types": 8,
        "email_files": 60,
    }


def test_all_profiled_csv_hashes_match_immutable_baseline() -> None:
    for profile in PROFILE["csv_profiles"]:
        assert digest(ROOT / "source_baseline" / profile["path"]) == profile["sha256"]


def test_only_relationship_issue_is_broken_deviation_event_links() -> None:
    issues = [row for row in PROFILE["relationships"] if row["issue_count"]]
    assert issues == [
        {
            "relationship": "deviation.linked_event_id -> event",
            "issue_count": 188,
            "expected": "0",
            "meaning": "Deviation evidence link resolves",
        }
    ]


def test_transport_event_ids_are_unique_but_semantic_retries_exist() -> None:
    events = PROFILE["events"]
    assert events["duplicate_event_id_groups"] == 0
    assert events["excess_semantic_duplicate_rows"] == 7
    assert events["max_recording_lag_hours"] == 12.0


def test_known_nulls_are_preserved_for_contextual_interpretation() -> None:
    by_path = {row["path"]: row for row in PROFILE["csv_profiles"]}
    assert by_path["data/raw/cryogenic_telemetry.csv"]["null_counts"]["temperature_c"] == 10
    assert by_path["data/raw/deviations.csv"]["null_counts"]["linked_event_id"] == 36
    assert by_path["data/raw/qc_results.csv"]["null_counts"]["unit"] == 3200
    assert by_path["data/raw/shipments.csv"]["null_counts"]["batch_id"] == 800


def test_shadow_email_headers_are_present_but_content_remains_untrusted() -> None:
    assert PROFILE["emails"]["files"] == 60
    assert PROFILE["emails"]["missing_required_header_files"] == 0
    assert PROFILE["emails"]["classification"] == "synthetic_untrusted_shadow_operations_evidence"
