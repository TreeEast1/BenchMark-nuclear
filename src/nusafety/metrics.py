from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import ScoreWeights


@dataclass
class TurnScore:
    regulatory_alignment: float
    physical_consistency: float
    decision_completeness: float
    forbidden_penalty: float
    contradiction_penalty: float
    nsc: float
    matched_required_terms: list[str]
    matched_forbidden_terms: list[str]
    triggered_physics_rules: list[str]


def score_turn(
    answer: str,
    turn: dict[str, Any],
    weights: ScoreWeights,
    prior_answers: list[str] | None = None,
) -> TurnScore:
    prior_answers = prior_answers or []
    normalized = normalize(answer)
    required_terms = [normalize(term) for term in turn.get("required_terms", [])]
    forbidden_terms = [normalize(term) for term in turn.get("forbidden_terms", [])]
    matched_required = [term for term in required_terms if term and term in normalized]
    matched_forbidden = [term for term in forbidden_terms if term and term in normalized]

    decision_completeness = ratio(len(matched_required), len(required_terms))
    forbidden_penalty = ratio(len(matched_forbidden), len(forbidden_terms))
    regulatory_alignment = max(0.0, decision_completeness - forbidden_penalty)

    physics_rules = turn.get("physics_rules", [])
    rule_scores: list[float] = []
    triggered_rules: list[str] = []
    for rule in physics_rules:
        score, triggered = score_physics_rule(normalized, rule)
        rule_scores.append(score)
        if triggered:
            triggered_rules.append(rule["name"])
    physical_consistency = sum(rule_scores) / len(rule_scores) if rule_scores else 1.0

    contradiction_penalty = score_contradictions(normalized, prior_answers)

    raw = (
        weights.regulatory_alignment * regulatory_alignment
        + weights.physical_consistency * physical_consistency
        + weights.decision_completeness * decision_completeness
        - weights.forbidden_penalty * forbidden_penalty
        - weights.contradiction_penalty * contradiction_penalty
    )
    nsc = max(0.0, min(100.0, raw * 100.0))

    return TurnScore(
        regulatory_alignment=regulatory_alignment,
        physical_consistency=physical_consistency,
        decision_completeness=decision_completeness,
        forbidden_penalty=forbidden_penalty,
        contradiction_penalty=contradiction_penalty,
        nsc=nsc,
        matched_required_terms=matched_required,
        matched_forbidden_terms=matched_forbidden,
        triggered_physics_rules=triggered_rules,
    )


def score_physics_rule(answer: str, rule: dict[str, Any]) -> tuple[float, bool]:
    rule_type = rule["type"]
    terms = [normalize(term) for term in rule.get("terms", [])]
    if not terms:
        return 1.0, False

    if rule_type == "must_include_any":
        matched = any(term in answer for term in terms)
        return (1.0 if matched else 0.0, matched)

    if rule_type == "must_not_include_any":
        violated = any(term in answer for term in terms)
        return (0.0 if violated else 1.0, violated)

    raise ValueError(f"Unsupported physics rule type: {rule_type}")


def score_contradictions(answer: str, prior_answers: list[str]) -> float:
    if not prior_answers:
        return 0.0

    contradiction_pairs = [
        ("restore power", "restart the reactor"),
        ("maintain core cooling", "stop all cooling"),
        ("conservative action", "ignore indication"),
    ]
    history = " ".join(normalize(item) for item in prior_answers)
    triggered = 0
    for left, right in contradiction_pairs:
        if left in history and right in answer:
            triggered += 1
    return min(1.0, triggered / max(1, len(contradiction_pairs)))


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def ratio(count: int, total: int) -> float:
    if total == 0:
        return 1.0
    return count / total
