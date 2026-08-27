import pytest

from src.infrastructure.viacep_client import ViaCepClient
from tests.unit.relationship.people.stubs import stub_viacep_payload


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict | None = None) -> None:
        self.status_code = status_code
        self._payload = payload or {}

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise pytest.fail(f"unexpected raise_for_status for {self.status_code}")


class _FakeClient:
    def __init__(self, response: _FakeResponse, expected_url: str | None = None) -> None:
        self._response = response
        self.expected_url = expected_url
        self.requested_url = None

    def __call__(self, timeout=None):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def get(self, url: str):
        self.requested_url = url
        if self.expected_url:
            assert url == self.expected_url
        return self._response


def test_fetch_normalizes_cep_and_returns_json(monkeypatch):
    fake_client = _FakeClient(
        _FakeResponse(200, stub_viacep_payload()),
        expected_url="https://viacep.com.br/ws/01001000/json/",
    )
    monkeypatch.setattr("src.infrastructure.viacep_client.httpx.Client", fake_client)
    client = ViaCepClient(base_url="https://viacep.com.br/ws/")
    payload = client.fetch("01001-000")
    assert payload["localidade"] == "São Paulo"


def test_fetch_rejects_invalid_cep_before_request():
    client = ViaCepClient()
    with pytest.raises(ValueError, match="8 digits"):
        client.fetch("123")


def test_fetch_raises_on_http_400(monkeypatch):
    fake_client = _FakeClient(_FakeResponse(400))
    monkeypatch.setattr("src.infrastructure.viacep_client.httpx.Client", fake_client)
    client = ViaCepClient(base_url="https://viacep.com.br/ws/")
    with pytest.raises(ValueError, match="Invalid CEP format"):
        client.fetch("01001000")
