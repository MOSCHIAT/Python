from pathlib import Path

from ai_toolkit.service import generate, save_response


def test_mock_provider():
    response = generate(
        "Explique Python",
        api_key=None,
        model="mock-model",
        timeout=1,
        mock=True,
    )
    assert response.provider == "mock"
    assert "Explique Python" in response.text


def test_save_response(tmp_path: Path):
    response = generate(
        "teste",
        api_key=None,
        model="mock-model",
        timeout=1,
        mock=True,
    )
    output = tmp_path / "response.json"
    save_response(response, "teste", output)
    content = output.read_text(encoding="utf-8")
    assert '"provider": "mock"' in content
    assert '"prompt": "teste"' in content
