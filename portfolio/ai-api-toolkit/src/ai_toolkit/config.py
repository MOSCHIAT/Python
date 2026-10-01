from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    model: str
    timeout: float

    @classmethod
    def from_environment(cls, model: str | None = None, timeout: float = 30.0) -> "Settings":
        return cls(
            api_key=os.getenv("GEMINI_API_KEY"),
            model=model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            timeout=timeout,
        )
