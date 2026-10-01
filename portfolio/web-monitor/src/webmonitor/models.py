from dataclasses import dataclass

@dataclass(frozen=True)
class PageSnapshot:
    url: str
    status_code: int
    title: str
    text: str
    content_hash: str

@dataclass(frozen=True)
class CheckResult:
    url: str
    status: str
    title: str
    content_hash: str
    status_code: int | None = None
    error: str | None = None
