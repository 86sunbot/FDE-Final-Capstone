#!/usr/bin/env python3
"""Validate internal consistency and safety invariants of the Stage 5 domain spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_ENVELOPE_FIELDS = {
    "event_id",
    "event_type",
    "schema_version",
    "aggregate_type",
    "aggregate_id",
    "sequence",
    "occurred_at",
    "recorded_at",
    "source_system",
    "evidence_refs",
    "correlation_id",
    "actor",
    "data_quality",
    "payload",
    "payload_digest",
    "classification",
    "trace_id",
}

CONSEQUENTIAL_EVENTS = {
    "IdentityResolutionApproved",
    "IdentityResolutionRejected",
    "IdentityResolutionApplied",
    "ProductReleased",
    "ProductReleaseRejected",
    "ReleaseDecisionSuperseded",
    "ApprovalRecorded",
}


def unique(values: list[str], label: str, errors: list[str]) -> None:
    if len(values) != len(set(values)):
        errors.append(f"{label} contains duplicates")


def validate(spec: dict) -> list[str]:
    errors: list[str] = []

    unique(spec["assessment_outcomes"], "assessment_outcomes", errors)
    unique(spec["identifier_types"], "identifier_types", errors)

    rules = spec["rules"]
    rule_ids = [rule["id"] for rule in rules]
    unique(rule_ids, "rule IDs", errors)
    for rule in rules:
        if rule.get("severity") not in {"P0", "P1", "P2"}:
            errors.append(f"{rule.get('id')} has invalid severity")
        for required in ("id", "severity", "owner", "statement"):
            if not rule.get(required):
                errors.append(f"rule missing {required}: {rule}")

    envelope = set(spec["event_envelope"]["required_fields"])
    missing_envelope = sorted(REQUIRED_ENVELOPE_FIELDS - envelope)
    if missing_envelope:
        errors.append(f"event envelope missing: {missing_envelope}")

    event_rows = spec["event_types"]
    event_names = [event["name"] for event in event_rows]
    unique(event_names, "event types", errors)
    event_by_name = {event["name"]: event for event in event_rows}
    for event_name in CONSEQUENTIAL_EVENTS:
        event = event_by_name.get(event_name)
        if not event:
            errors.append(f"missing consequential event: {event_name}")
        elif event.get("authority_required") is not True:
            errors.append(f"consequential event lacks authority: {event_name}")

    for machine_name, machine in spec["state_machines"].items():
        states = machine["states"]
        unique(states, f"{machine_name} states", errors)
        state_set = set(states)
        if machine["initial"] not in state_set:
            errors.append(f"{machine_name} initial state is not declared")
        transition_keys: list[tuple[str, str, str, str]] = []
        for transition in machine["transitions"]:
            source = transition.get("from")
            target = transition.get("to")
            event_name = transition.get("event")
            guard = transition.get("guard")
            if source not in state_set:
                errors.append(f"{machine_name} transition has unknown source: {source}")
            if target not in state_set:
                errors.append(f"{machine_name} transition has unknown target: {target}")
            if event_name not in event_by_name:
                errors.append(f"{machine_name} transition has undeclared event: {event_name}")
            if not guard:
                errors.append(f"{machine_name} transition lacks guard: {source}->{target}")
            if not isinstance(transition.get("authority_required"), bool):
                errors.append(f"{machine_name} transition lacks authority flag: {source}->{target}")
            if event_name in CONSEQUENTIAL_EVENTS and transition.get("authority_required") is not True:
                errors.append(f"{machine_name} consequential transition lacks authority: {event_name}")
            transition_keys.append((source, target, event_name, guard))
        unique(transition_keys, f"{machine_name} transitions", errors)

    quality = spec["state_machines"]["quality_release"]["transitions"]
    approvals = [row for row in quality if row["to"] == "APPROVED"]
    if len(approvals) != 1 or approvals[0]["event"] != "ProductReleased" or not approvals[0]["authority_required"]:
        errors.append("quality release APPROVED must have exactly one authorized ProductReleased path")

    identity = spec["state_machines"]["identity_case"]["transitions"]
    identity_approvals = [row for row in identity if row["to"] == "APPROVED"]
    if len(identity_approvals) != 1 or identity_approvals[0]["event"] != "IdentityResolutionApproved" or not identity_approvals[0]["authority_required"]:
        errors.append("identity APPROVED must have exactly one authorized IdentityResolutionApproved path")

    recommendation_transitions = [
        (machine_name, row)
        for machine_name, machine in spec["state_machines"].items()
        for row in machine["transitions"]
        if row["event"] == "RecommendationGenerated"
    ]
    if recommendation_transitions:
        errors.append("RecommendationGenerated must not transition a domain aggregate")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", nargs="?", type=Path, default=Path("docs/stages/stage_05/domain_spec.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    errors = validate(spec)
    if errors:
        print(json.dumps({"status": "FAILED", "errors": errors}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "rules": len(spec["rules"]),
                "event_types": len(spec["event_types"]),
                "state_machines": len(spec["state_machines"]),
                "transitions": sum(len(machine["transitions"]) for machine in spec["state_machines"].values()),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
