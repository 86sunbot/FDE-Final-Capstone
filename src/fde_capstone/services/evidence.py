from __future__ import annotations

from typing import Any

from ..model import Assessment, Outcome
from ..storage import Database


class EvidenceService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def register(self, evidence_id: str, source: str, locator: str, payload: dict[str, Any], occurred_at: str, recorded_at: str | None = None) -> str:
        return self.db.add_evidence(evidence_id, source, locator, payload, occurred_at, recorded_at)

    def exists(self, evidence_ids: list[str] | tuple[str, ...]) -> bool:
        if not evidence_ids:
            return False
        placeholders = ",".join("?" for _ in evidence_ids)
        row = self.db.connection.execute(f"SELECT COUNT(*) AS n FROM evidence WHERE evidence_id IN ({placeholders})", tuple(evidence_ids)).fetchone()
        return int(row["n"]) == len(set(evidence_ids))

    def bitemporal_assert(self, assertion_id: str, subject: str, attribute: str, value: Any, source: str, occurred_at: str, recorded_at: str, evidence_id: str) -> None:
        if not self.exists([evidence_id]):
            raise ValueError("UNKNOWN_EVIDENCE")
        self.db.add_assertion(assertion_id, subject, attribute, value, source, occurred_at, recorded_at, evidence_id)

    def known_at(self, subject: str, cutoff: str) -> list[dict]:
        return self.db.assertions_known_at(subject, cutoff)


def combine_prerequisites(prerequisites: dict[str, tuple[Outcome, list[str]]], rule_versions: tuple[str, ...]) -> Assessment:
    blockers = tuple(name for name, (outcome, _) in prerequisites.items() if outcome == Outcome.NOT_SATISFIED)
    unknowns = tuple(name for name, (outcome, _) in prerequisites.items() if outcome == Outcome.UNKNOWN)
    evidence = tuple(sorted({item for _, refs in prerequisites.values() for item in refs}))
    if blockers:
        outcome = Outcome.NOT_SATISFIED
    elif unknowns or any(not refs for _, refs in prerequisites.values()):
        outcome = Outcome.UNKNOWN
        unknowns = tuple(sorted(set(unknowns) | {name for name, (_, refs) in prerequisites.items() if not refs}))
    else:
        outcome = Outcome.SATISFIED
    return Assessment(outcome, evidence, blockers, unknowns, rule_versions)
