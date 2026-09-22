from __future__ import annotations

from ..model import Assessment, Outcome, Principal
from ..security import require
from ..storage import Database
from .evidence import EvidenceService, combine_prerequisites


class ReadinessService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.evidence = EvidenceService(db)

    def assess(
        self,
        principal: Principal,
        journey_id: str,
        milestone: str,
        prerequisites: dict[str, tuple[Outcome, list[str]]],
    ) -> Assessment:
        require(principal, "read", journey_id)
        required = {
            "PRE_COLLECTION": {"identity", "consent", "authorization", "site"},
            "MATERIAL_RECEIPT": {"identity", "custody", "shipment"},
            "INFUSION": {"identity", "consent", "product_release", "receipt", "clinical_authority"},
        }.get(milestone)
        if required is None:
            raise ValueError("UNKNOWN_MILESTONE")
        missing = required - set(prerequisites)
        normalized = dict(prerequisites)
        for name in missing:
            normalized[name] = (Outcome.UNKNOWN, [])
        result = combine_prerequisites(normalized, (f"READINESS-{milestone}-v1",))
        if result.evidence_refs and not self.evidence.exists(result.evidence_refs):
            return Assessment(Outcome.UNKNOWN, result.evidence_refs, result.blockers, tuple(sorted(set(result.unknowns) | {"unresolved_evidence_reference"})), result.rule_versions)
        self.db.metric(f"readiness_{result.outcome.value.lower()}")
        return result
