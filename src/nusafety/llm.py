from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Any

import requests

from .config import ModelConfig


@dataclass
class ChatMessage:
    role: str
    content: str


class OpenAICompatibleClient:
    def __init__(self, config: ModelConfig) -> None:
        self.config = config
        api_key = os.environ.get(config.api_key_env)
        if not api_key:
            raise RuntimeError(f"Environment variable {config.api_key_env} is not set.")
        self.api_key = api_key

    def chat(self, messages: list[ChatMessage]) -> str:
        payload: dict[str, Any] = {
            "model": self.config.model_name,
            "messages": [asdict(message) for message in messages],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }
        response = requests.post(
            f"{self.config.api_base.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        body = response.json()
        return body["choices"][0]["message"]["content"].strip()
