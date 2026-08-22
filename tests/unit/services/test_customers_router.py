from unittest.mock import MagicMock

import httpx
import pytest
from fastapi import HTTPException

from src.services.routers import customers_router
from src.services.routers.customers_router import (
    get_or_create_address,
    get_or_create_person,
    lookup_cep,
    require_person_by_cpf,
)
from tests.unit.relationship.people.stubs import stub_address, stub_person, stub_viacep_payload


def test_require_person_by_cpf_raises_when_missing():
    session = MagicMock()
    session.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        require_person_by_cpf(session, "12345678901")
    assert exc.value.status_code == 400
    assert "people table" in exc.value.detail


def test_require_person_by_cpf_returns_person():
    session = MagicMock()
    person = MagicMock()
    session.get.return_value = person
    assert require_person_by_cpf(session, "12345678901") is person


def test_get_or_create_person_inserts_when_missing():
    session = MagicMock()
    session.get.return_value = None
    get_or_create_person(session, stub_person())
    session.add.assert_called_once()
    session.flush.assert_called_once()


def test_get_or_create_person_returns_existing():
    session = MagicMock()
    existing = MagicMock()
    session.get.return_value = existing
    result = get_or_create_person(session, stub_person())
    assert result is existing
    session.add.assert_not_called()


def test_get_or_create_address_inserts_when_missing():
    session = MagicMock()
    session.get.return_value = None
    get_or_create_address(session, stub_address())
    session.add.assert_called_once()
    session.commit.assert_called_once()


def test_get_or_create_address_returns_existing():
    session = MagicMock()
    existing = MagicMock()
    session.get.return_value = existing
    result = get_or_create_address(session, stub_address())
    assert result is existing
    session.add.assert_not_called()


def test_lookup_cep_saves_address(monkeypatch):
    monkeypatch.setattr(
        customers_router.viacep_client,
        "fetch",
        lambda cep: stub_viacep_payload(),
    )
    session = MagicMock()
    session.get.return_value = None
    address = lookup_cep("01001000", session)
    assert address.cep_id == "01001000"
    assert address.city == "São Paulo"
    session.add.assert_called_once()


def test_lookup_cep_returns_404_when_not_found(monkeypatch):
    monkeypatch.setattr(
        customers_router.viacep_client,
        "fetch",
        lambda cep: {"erro": True},
    )
    with pytest.raises(HTTPException) as exc:
        lookup_cep("99999999", MagicMock())
    assert exc.value.status_code == 404


def test_lookup_cep_returns_502_when_viacep_unavailable(monkeypatch):
    def _raise(_cep):
        raise httpx.ConnectError("connection failed")

    monkeypatch.setattr(customers_router.viacep_client, "fetch", _raise)
    with pytest.raises(HTTPException) as exc:
        lookup_cep("01001000", MagicMock())
    assert exc.value.status_code == 502
