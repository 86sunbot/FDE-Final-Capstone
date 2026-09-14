from __future__ import annotations

import json
import uuid
from typing import Any, Protocol

from ..model import canonical_json, utc_now
from ..storage import Database
from .common import correlation


class RecommendationProvider(Protocol):
    model_name: str

    def recommend(self, context: dict[str, Any]) -> Any: ...


ALLOWED_KEYS = {"summary", "evidence_refs", "uncertainty", "next_actions"}
PROHIBITED_KEYS = {"approved", "authority", "canonical_state", "execute", "identity_link", "product_disposition", "release_decision", "tool_call"}


class AssistantGateway:
    def __init__(self, db: Database, provider: RecommendationProvider | None = None) -> None:
        self.db = db
        self.provider = provider

    @staticmethod
    def validate(output: Any, available_evidence: set[str]) -> tuple[bool, str | None]:
        if not isinstance(output, dict):
            return False, "NOT_AN_OBJECT"
        keys = set(output)
        if keys & PROHIBITED_KEYS:
            return False, "PROHIBITED_AUTHORITY_OR_TOOL_FIELD"
        if keys != ALLOWED_KEYS:
            return False, "SCHEMA_INVALID"
        if not isinstance(output["summary"], str) or not output["summary"].strip():
            return False, "SCHEMA_INVALID"
        if not isinstance(output["evidence_refs"], list) or not output["evidence_refs"]:
            return False, "EVIDENCE_REFERENCE_INVALID"
        if not set(output["evidence_refs"]) <= available_evidence:
            return False, "EVIDENCE_REFERENCE_INVALID"
        if not isinstance(output["uncertainty"], list) or not isinstance(output["next_actions"], list):
            return False, "SCHEMA_INVALID"
        return True, None

    def recommend(self, scope: str, deterministic_context: dict[str, Any], correlation_id: str | None = None) -> dict:
        trace = correlation(correlation_id)
        recommendation_id = f"REC-{uuid.uuid4()}"
        available = set(deterministic_context.get("available_evidence", []))
        mode = "DETERMINISTIC_ONLY"
        output = None
        rejection = "AI_DISABLED"
        if self.provider is not None:
            try:
                candidate = self.provider.recommend(deterministic_context)
                valid, rejection = self.validate(candidate, available)
                if valid:
                    mode = "BOUNDED_AI"
                    output = candidate
                    rejection = None
            except Exception:
                rejection = "AI_UNAVAILABLE"
        with self.db._lock, self.db.connection:
            self.db.connection.execute(
                "INSERT INTO recommendations VALUES(?,?,?,?,?,?,?,?)",
                (recommendation_id, scope, mode, canonical_json(output) if output else None, rejection, canonical_json(sorted(available)), utc_now(), trace),
            )
        self.db.audit("ASSISTANT_GATEWAY", "recommendation:create", scope, mode, {"recommendation_id": recommendation_id, "rejection_reason": rejection}, trace)
        self.db.metric("recommendation_requests")
        if rejection:
            self.db.metric("recommendation_fallbacks")
        return {
            "recommendation_id": recommendation_id,
            "mode": mode,
            "deterministic_context": deterministic_context,
            "recommendation": output,
            "rejection_reason": rejection,
        }
