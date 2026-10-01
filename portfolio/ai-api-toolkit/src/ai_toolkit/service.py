from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path

from .client import AIResponse, GeminiClient


class MockClient:
    def __init__(self, model: str = "mock-model"):
        self.model = model

    def generate(self, prompt: str) -> AIResponse:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        return AIResponse(
            provider="mock",
            model=self.model,
            text=f"[MOCK] Recebi o prompt: {prompt}",
        )


def generate(
    prompt: str,
    *,
    api_key: str | None,
    model: str,
    timeout: float,
    mock: bool,
) -> AIResponse:
    client = MockClient(model) if mock else GeminiClient(
        api_key=api_key or "",
        model=model,
        timeout=timeout,
    )
    return client.generate(prompt)


def save_response(response: AIResponse, prompt: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": response.provider,
        "model": response.model,
        "prompt": prompt,
        "response": response.text,
    }
    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def response_dict(response: AIResponse) -> dict[str, str]:
    return asdict(response)
