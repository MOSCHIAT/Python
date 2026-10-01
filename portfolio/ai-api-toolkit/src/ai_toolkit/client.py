from __future__ import annotations

from dataclasses import dataclass
import json
from urllib import error, request


class AIClientError(RuntimeError):
    """Raised when an AI provider cannot complete a request."""


@dataclass(frozen=True)
class AIResponse:
    provider: str
    model: str
    text: str


class GeminiClient:
    endpoint_template = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def __init__(self, api_key: str, model: str, timeout: float = 30.0):
        if not api_key.strip():
            raise ValueError("API key cannot be empty")
        if not model.strip():
            raise ValueError("Model cannot be empty")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str) -> AIResponse:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.endpoint_template.format(model=self.model),
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise AIClientError(f"Gemini HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise AIClientError(f"Network error: {exc.reason}") from exc
        except TimeoutError as exc:
            raise AIClientError("Request timed out") from exc

        try:
            data = json.loads(raw)
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise AIClientError("Unexpected Gemini response format") from exc

        return AIResponse(provider="gemini", model=self.model, text=text)
