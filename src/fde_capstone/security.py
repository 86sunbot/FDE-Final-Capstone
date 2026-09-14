from __future__ import annotations

from dataclasses import dataclass

from .model import Principal


class AuthorizationError(PermissionError):
    pass


ROLE_ACTIONS = {
    "ADMIN": {"read", "case:create", "identity:decide", "slot:command", "slot:reconcile", "quality:release", "audit:verify"},
    "COORDINATOR": {"read", "case:create"},
    "IDENTITY_AUTHORITY": {"read", "identity:decide"},
    "PLANNER": {"read", "slot:command", "slot:reconcile"},
    "QUALITY_AUTHORITY": {"read", "quality:release"},
    "VIEWER": {"read"},
}


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str


def decide(principal: Principal | None, action: str, scope: str) -> AuthorizationDecision:
    if principal is None:
        return AuthorizationDecision(False, "MISSING_PRINCIPAL")
    if "*" not in principal.scopes and scope not in principal.scopes:
        return AuthorizationDecision(False, "SCOPE_DENIED")
    allowed = any(action in ROLE_ACTIONS.get(role, set()) for role in principal.roles)
    return AuthorizationDecision(allowed, "ALLOWED" if allowed else "ROLE_DENIED")


def require(principal: Principal | None, action: str, scope: str) -> None:
    result = decide(principal, action, scope)
    if not result.allowed:
        raise AuthorizationError(result.reason)
