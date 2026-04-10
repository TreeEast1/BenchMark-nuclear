from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from statistics import mean
from typing import Any

from .config import AppConfig
from .llm import ChatMessage, OpenAICompatibleClient
from .metrics import score_turn


class EvaluationRunner:
    def __init__(self, config: AppConfig, output_dir: Path) -> None:
        self.config = config
        self.output_dir = output_dir
        self.client = OpenAICompatibleClient(config.model)

    def run(self, cases: list[dict[str, Any]]) -> dict[str, float]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        all_scores: list[float] = []
        score_path = self.output_dir / "scores.jsonl"
        transcript_path = self.output_dir / "transcripts.jsonl"

        with score_path.open("w", encoding="utf-8") as score_handle:
            transcript_handle = (
                transcript_path.open("w", encoding="utf-8")
                if self.config.evaluation.save_transcript
                else None
            )
            try:
                for case in cases:
                    transcript = self.run_case(case)
                    for turn_result in transcript["turns"]:
                        all_scores.append(turn_result["score"]["nsc"])
                        score_handle.write(json.dumps(turn_result, ensure_ascii=False) + "\n")
                    if transcript_handle is not None:
                        transcript_handle.write(json.dumps(transcript, ensure_ascii=False) + "\n")
            finally:
                if transcript_handle is not None:
                    transcript_handle.close()

        return {
            "scenario_count": len(cases),
            "mean_nsc": mean(all_scores) if all_scores else 0.0,
        }

    def run_case(self, case: dict[str, Any]) -> dict[str, Any]:
        messages = [ChatMessage(role="system", content=case["system_prompt"])]
        prior_answers: list[str] = []
        turns_out: list[dict[str, Any]] = []

        for turn in case["turns"]:
            messages.append(ChatMessage(role="user", content=turn["user"]))
            answer = self.client.chat(messages)
            messages.append(ChatMessage(role="assistant", content=answer))
            score = score_turn(
                answer=answer,
                turn=turn,
                weights=self.config.evaluation.score_weights,
                prior_answers=prior_answers,
            )
            prior_answers.append(answer)
            turns_out.append(
                {
                    "scenario_id": case["scenario_id"],
                    "title": case.get("title", ""),
                    "turn_id": turn["turn_id"],
                    "user": turn["user"],
                    "assistant": answer,
                    "score": asdict(score),
                }
            )

        return {
            "scenario_id": case["scenario_id"],
            "title": case.get("title", ""),
            "turns": turns_out,
        }
