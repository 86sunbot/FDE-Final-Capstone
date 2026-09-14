from __future__ import annotations

from typing import Any


class DeterministicAssistantFake:
    """Repeatable provider substitute; it is not represented as a real language model."""

    model_name = "deterministic-fake-v1"

    def recommend(self, context: dict[str, Any]) -> dict[str, Any]:
        evidence = list(context.get("available_evidence", []))
        blockers = list(context.get("blockers", []))
        unknowns = list(context.get("unknowns", []))
        summary = "Review required." if blockers or unknowns else "No deterministic blocker is currently recorded."
        return {
            "summary": summary,
            "evidence_refs": evidence,
            "uncertainty": unknowns,
            "next_actions": ["Review cited deterministic evidence", "Escalate unresolved blockers"] if blockers or unknowns else ["Continue through the authorized deterministic workflow"],
        }


class FailingAssistantFake:
    model_name = "failing-fake-v1"

    def recommend(self, context: dict[str, Any]) -> dict[str, Any]:
        raise TimeoutError("simulated model timeout")
