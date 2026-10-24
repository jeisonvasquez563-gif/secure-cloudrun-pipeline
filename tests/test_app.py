import pytest
from fastapi.testclient import TestClient

from app.main import SECURITY_HEADERS, app

client = TestClient(app)


def test_healthz_returns_ok() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_is_reported() -> None:
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


@pytest.mark.parametrize("path", ["/healthz", "/version", "/does-not-exist"])
def test_security_headers_are_on_every_response(path: str) -> None:
    response = client.get(path)
    for name, value in SECURITY_HEADERS.items():
        assert response.headers[name] == value


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_interactive_docs_are_not_exposed(path: str) -> None:
    assert client.get(path).status_code == 404
