"""Small executable probes for the proposed deterministic-plus-bounded-AI option.

This is option evidence, not the Stage 14 implementation.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable


PROHIBITED_AI_KEYS = {
    "approved",
    "authority",
    "canonical_state",
    "execute",
    "identity_link",
    "product_disposition",
    "release_decision",
}
ALLOWED_AI_KEYS = {"summary", "evidence_refs", "uncertainty", "next_actions"}


def canonical_digest(command_type: str, scope: str, payload: dict[str, Any]) -> str:
    document = {"command_type": command_type, "scope": scope, "payload": payload}
    wire = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(wire.encode("utf-8")).hexdigest()


def register_command(
    ledger: dict[str, dict[str, Any]],
    key: str,
    command_type: str,
    scope: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Bind one idempotency key to one canonical command and return stored replay."""
    digest = canonical_digest(command_type, scope, payload)
    existing = ledger.get(key)
    if existing:
        if existing["digest"] != digest:
            return {"decision": "IDEMPOTENCY_CONFLICT", "dispatch": False}
        return {"decision": "REPLAY_STORED", "dispatch": False, "command": existing}
    command = {"key": key, "digest": digest, "state": "DISPATCH_PENDING", "effect_count": 0}
    ledger[key] = command
    return {"decision": "ACCEPTED", "dispatch": True, "command": command}


def record_ambiguous_timeout(command: dict[str, Any]) -> None:
    """A timeout after dispatch never becomes an automatic retry."""
    command["state"] = "OUTCOME_UNKNOWN"


def may_retry(command: dict[str, Any]) -> bool:
    return command.get("state") == "FAILED_RETRYABLE" and command.get("retry_authorized") is True


def project_quality_release(assertions: list[dict[str, Any]]) -> dict[str, Any]:
    """Only an authoritative QMS ProductReleased assertion can approve release."""
    conflicts = [item for item in assertions if item.get("source_system") in {"MES", "ERP"} and item.get("status") in {"RELEASED", "AVAILABLE", "MFG_COMPLETE"}]
    approved = [
        item
        for item in assertions
        if item.get("source_system") == "QMS"
        and item.get("event_type") == "ProductReleased"
        and item.get("authority_valid") is True
        and item.get("evidence_refs")
    ]
    if approved:
        return {"state": "PRODUCT_RELEASED", "evidence_refs": approved[-1]["evidence_refs"], "conflicts": conflicts}
    return {"state": "UNKNOWN_OR_AWAITING_QUALITY", "evidence_refs": [], "conflicts": conflicts}


def known_assertions_at(assertions: list[dict[str, Any]], recorded_cutoff: str) -> list[str]:
    """Return assertion IDs known at a recorded-time cutoff, ordered by valid time."""
    cutoff = datetime.fromisoformat(recorded_cutoff)
    known = [item for item in assertions if datetime.fromisoformat(item["recorded_at"]) <= cutoff]
    return [item["assertion_id"] for item in sorted(known, key=lambda item: (item["occurred_at"], item["recorded_at"], item["assertion_id"]))]


@dataclass(frozen=True)
class RecommendationResult:
    mode: str
    deterministic_context: dict[str, Any]
    recommendation: dict[str, Any] | None
    rejection_reason: str | None = None


def validate_recommendation(output: Any, available_evidence: set[str]) -> tuple[bool, str | None]:
    if not isinstance(output, dict):
        return False, "NOT_AN_OBJECT"
    keys = set(output)
    if keys & PROHIBITED_AI_KEYS:
        return False, "PROHIBITED_AUTHORITY_FIELD"
    if not keys <= ALLOWED_AI_KEYS or not {"summary", "evidence_refs", "uncertainty"} <= keys:
        return False, "SCHEMA_INVALID"
    refs = output.get("evidence_refs")
    if not isinstance(refs, list) or not refs or not set(refs) <= available_evidence:
        return False, "EVIDENCE_REFERENCE_INVALID"
    if not isinstance(output.get("summary"), str) or not isinstance(output.get("uncertainty"), list):
        return False, "SCHEMA_INVALID"
    return True, None


def assist_or_fallback(
    deterministic_context: dict[str, Any],
    model_call: Callable[[dict[str, Any]], Any] | None,
) -> RecommendationResult:
    """AI is replaceable: absent, failed or invalid AI leaves deterministic context intact."""
    if model_call is None:
        return RecommendationResult("DETERMINISTIC_ONLY", deterministic_context, None, "AI_DISABLED")
    try:
        output = model_call(deterministic_context)
    except Exception:
        return RecommendationResult("DETERMINISTIC_ONLY", deterministic_context, None, "AI_UNAVAILABLE")
    valid, reason = validate_recommendation(output, set(deterministic_context.get("available_evidence", [])))
    if not valid:
        return RecommendationResult("DETERMINISTIC_ONLY", deterministic_context, None, reason)
    return RecommendationResult("BOUNDED_AI", deterministic_context, output)
