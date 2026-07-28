#!/usr/bin/env python3
"""Validate a PBS assurance state register and report the next governed gate."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

VALID_GATES = {
    "development",
    "internal_verification",
    "independent_review",
    "controlled_trial",
    "recalibration",
    "production_candidate",
    "production",
}

MANDATORY_INTERNAL = (
    "unit_tests_passed",
    "integration_tests_passed",
    "policy_boundaries_passed",
    "eligibility_none_safety_passed",
    "adversarial_tests_passed",
    "report_integrity_passed",
    "protected_hashes_passed",
    "independent_checksums_passed",
    "determinism_passed",
)


def load_state(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        state = json.load(handle)
    if not isinstance(state, dict):
        raise ValueError("State root must be a JSON object")
    return state


def evidence_weight(item: dict[str, Any]) -> float:
    weight = float(item.get("weight", 1.0))
    if not 0.0 <= weight <= 1.0:
        raise ValueError("Evidence weight must be between 0 and 1")
    independence = item.get("independence", "builder_generated")
    discount = {
        "independent": 1.0,
        "untouched_holdout": 0.8,
        "builder_generated": 0.35,
        "duplicated_or_correlated": 0.15,
    }.get(independence)
    if discount is None:
        raise ValueError(f"Unknown evidence independence class: {independence}")
    return weight * discount


def posterior(state: dict[str, Any]) -> tuple[float, float, float, float]:
    ledger = state.get("bayesian_ledger", {})
    alpha = float(ledger.get("prior_alpha", 1.0))
    beta = float(ledger.get("prior_beta", 1.0))
    if alpha <= 0 or beta <= 0:
        raise ValueError("Bayesian prior parameters must be positive")

    for item in ledger.get("evidence", []):
        successes = float(item.get("successes", 0))
        failures = float(item.get("failures", 0))
        if successes < 0 or failures < 0:
            raise ValueError("Evidence counts cannot be negative")
        weight = evidence_weight(item)
        alpha += successes * weight
        beta += failures * weight

    mean = alpha / (alpha + beta)
    variance = alpha * beta / (((alpha + beta) ** 2) * (alpha + beta + 1))
    conservative = max(0.0, mean - 1.96 * math.sqrt(variance))
    return alpha, beta, mean, conservative


def validate(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    gate = state.get("current_gate")
    if gate not in VALID_GATES:
        errors.append(f"Invalid current_gate: {gate!r}")

    verification = state.get("latest_verification", {})
    if verification.get("critical_defects_open", 0) < 0:
        errors.append("critical_defects_open cannot be negative")

    authorizations = state.get("human_authorizations", {})
    prohibited = set(state.get("prohibited_actions", []))
    if not authorizations.get("controlled_trial", False):
        for action in ("live_job_search", "controlled_trial"):
            if action not in prohibited:
                errors.append(f"{action} must remain prohibited without human authorization")
    if not authorizations.get("production", False) and "production_deployment" not in prohibited:
        errors.append("production_deployment must remain prohibited without human authorization")

    review_status = state.get("independent_review", {}).get("status", "pending")
    if gate == "controlled_trial":
        if review_status != "approved_for_controlled_trial":
            errors.append("Controlled trial requires independent approval")
        if not authorizations.get("controlled_trial", False):
            errors.append("Controlled trial requires explicit human authorization")
    return errors


def next_gate(state: dict[str, Any]) -> tuple[str, list[str]]:
    gate = state["current_gate"]
    verification = state.get("latest_verification", {})
    blockers: list[str] = []

    if gate in {"development", "internal_verification"}:
        blockers.extend(key for key in MANDATORY_INTERNAL if verification.get(key) is not True)
        if verification.get("critical_defects_open", 0):
            blockers.append("critical_defects_open")
        return ("independent_review" if not blockers else "internal_verification", blockers)

    if gate == "independent_review":
        review = state.get("independent_review", {}).get("status", "pending")
        if review != "approved_for_controlled_trial":
            blockers.append("independent_review_approval")
        if not state.get("human_authorizations", {}).get("controlled_trial", False):
            blockers.append("human_controlled_trial_authorization")
        return ("controlled_trial" if not blockers else "independent_review", blockers)

    if gate == "production_candidate":
        if not state.get("human_authorizations", {}).get("production", False):
            blockers.append("human_production_authorization")
        return ("production" if not blockers else gate, blockers)

    return gate, blockers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        state = load_state(args.state)
        errors = validate(state)
        alpha, beta, mean, conservative = posterior(state)
        proposed_gate, blockers = next_gate(state) if not errors else (
            state.get("current_gate", "unknown"),
            [],
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    result = {
        "valid": not errors,
        "current_gate": state.get("current_gate"),
        "proposed_gate": proposed_gate,
        "blockers": blockers,
        "errors": errors,
        "bayesian_ledger": {
            "posterior_alpha": round(alpha, 4),
            "posterior_beta": round(beta, 4),
            "posterior_mean": round(mean, 4),
            "normal_approx_95pct_lower_bound": round(conservative, 4),
            "note": "Evidence estimate only; never automatic authorization.",
        },
        "next_authorized_action": state.get("next_authorized_action"),
        "prohibited_actions": state.get("prohibited_actions", []),
    }
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"State valid: {result['valid']}")
        print(f"Gate: {result['current_gate']} -> {result['proposed_gate']}")
        print(f"Blockers: {', '.join(blockers) if blockers else 'none'}")
        print(
            "Readiness evidence: "
            f"mean={mean:.3f}, conservative lower bound={conservative:.3f}"
        )
        if errors:
            print("Errors:")
            for error in errors:
                print(f"- {error}")
        print(f"Next authorized action: {result['next_authorized_action']}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
