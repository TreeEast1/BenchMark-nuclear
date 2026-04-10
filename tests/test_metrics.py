from nusafety.config import ScoreWeights
from nusafety.metrics import score_turn


def test_score_turn_rewards_required_terms() -> None:
    weights = ScoreWeights()
    turn = {
        "required_terms": ["core cooling", "decay heat"],
        "forbidden_terms": ["restart the reactor"],
        "physics_rules": [
            {"name": "heat removal", "type": "must_include_any", "terms": ["decay heat"]}
        ],
    }
    answer = "Maintain core cooling and remove decay heat while restoring reliable power."
    score = score_turn(answer, turn, weights)
    assert score.decision_completeness == 1.0
    assert score.forbidden_penalty == 0.0
    assert score.nsc > 70.0


def test_score_turn_penalizes_forbidden_terms() -> None:
    weights = ScoreWeights()
    turn = {
        "required_terms": ["core cooling"],
        "forbidden_terms": ["restart the reactor"],
        "physics_rules": [],
    }
    answer = "Maintain core cooling and restart the reactor as soon as possible."
    score = score_turn(answer, turn, weights)
    assert score.forbidden_penalty == 1.0
    assert score.nsc < 80.0

