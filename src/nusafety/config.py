from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ModelConfig:
    api_base: str
    api_key_env: str
    model_name: str
    timeout_seconds: int = 120
    temperature: float = 0.1
    max_tokens: int = 1000


@dataclass
class ScoreWeights:
    regulatory_alignment: float = 0.45
    physical_consistency: float = 0.35
    decision_completeness: float = 0.20
    forbidden_penalty: float = 0.20
    contradiction_penalty: float = 0.15


@dataclass
class EvaluationConfig:
    output_name: str = "baseline_run"
    save_transcript: bool = True
    score_weights: ScoreWeights = field(default_factory=ScoreWeights)


@dataclass
class AppConfig:
    model: ModelConfig
    evaluation: EvaluationConfig


def load_config(path: Path) -> AppConfig:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    model = ModelConfig(**payload["model"])
    evaluation_payload = payload.get("evaluation", {})
    weights_payload = evaluation_payload.get("score_weights", {})
    evaluation = EvaluationConfig(
        output_name=evaluation_payload.get("output_name", "baseline_run"),
        save_transcript=evaluation_payload.get("save_transcript", True),
        score_weights=ScoreWeights(**weights_payload),
    )
    return AppConfig(model=model, evaluation=evaluation)
