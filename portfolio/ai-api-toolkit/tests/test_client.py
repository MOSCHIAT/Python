import pytest

from ai_toolkit.client import GeminiClient


def test_empty_key_is_rejected():
    with pytest.raises(ValueError):
        GeminiClient("", "gemini-3.8-flash")


def test_empty_prompt_is_rejected(monkeypatch):
    client = GeminiClient("fake-key", "gemini-3.8-flash")
    with pytest.raises(ValueError):
        client.generate("")


def test_payload_shape(monkeypatch):
    client = GeminiClient("fake-key", "gemini-3.8-flash")

    def fake_urlopen(req, timeout):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b'{"candidates":[{"content":{"parts":[{"text":"ok"}]}}]}'

        assert req.method == "POST"
        assert req.headers["X-goog-api-key"] == "fake-key"
        return Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    response = client.generate("hello")
    assert response.text == "ok"
    assert response.provider == "gemini"
