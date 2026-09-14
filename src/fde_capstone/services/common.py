from __future__ import annotations

import uuid

from ..model import Principal
from ..security import AuthorizationError, require
from ..storage import Database


def correlation(value: str | None = None) -> str:
    return value or f"TRACE-{uuid.uuid4()}"


def authorize(db: Database, principal: Principal | None, action: str, scope: str, correlation_id: str) -> None:
    try:
        require(principal, action, scope)
    except AuthorizationError as exc:
        db.audit(principal, action, scope, "DENIED", {"reason": str(exc)}, correlation_id)
        db.metric("authorization_denied")
        raise
