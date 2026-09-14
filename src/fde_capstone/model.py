from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class Outcome(StrEnum):
    SATISFIED = "SATISFIED"
    NOT_SATISFIED = "NOT_SATISFIED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class CommandState(StrEnum):
    DISPATCH_PENDING = "DISPATCH_PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED_RETRYABLE = "FAILED_RETRYABLE"
    FAILED_FINAL = "FAILED_FINAL"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"
    RECONCILING = "RECONCILING"
    COMPENSATION_PENDING = "COMPENSATION_PENDING"
    COMPENSATED = "COMPENSATED"


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[str]
    scopes: frozenset[str] = field(default_factory=lambda: frozenset({"*"}))


@dataclass(frozen=True)
class Assessment:
    outcome: Outcome
    evidence_refs: tuple[str, ...]
    blockers: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    rule_versions: tuple[str, ...] = ()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
