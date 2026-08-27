import pytest
from pydantic import ValidationError

from src.domain.customers_and_services.relationship.entities import Address
from tests.unit.relationship.people.stubs import stub_address, stub_viacep_payload


def test_create_address():
    address = stub_address()
    assert address.cep_id == "01001000"
    assert address.city == "São Paulo"
    assert address.state == "SP"


def test_cep_strips_hyphen():
    address = Address(
        cep_id="01001-000",
        street="Praça da Sé",
        neighborhood="Sé",
        city="São Paulo",
        state="sp",
    )
    assert address.cep_id == "01001000"
    assert address.state == "SP"


def test_cep_rejects_non_numeric():
    with pytest.raises(ValidationError, match="8 digits"):
        Address(cep_id="01001A00", city="São Paulo", state="SP")


def test_cep_rejects_wrong_length():
    with pytest.raises(ValidationError, match="8 digits"):
        Address(cep_id="123", city="São Paulo", state="SP")


def test_from_viacep_maps_payload():
    address = Address.from_viacep(stub_viacep_payload())
    assert address.cep_id == "01001000"
    assert address.street == "Praça da Sé"
    assert address.neighborhood == "Sé"
    assert address.city == "São Paulo"
    assert address.state == "SP"


def test_from_viacep_raises_when_cep_not_found():
    with pytest.raises(ValueError, match="not found"):
        Address.from_viacep({"erro": True})


def test_validate_viacep_response_rejects_mismatched_cep():
    address = stub_address()
    payload = stub_viacep_payload()
    payload["cep"] = "01310-100"
    with pytest.raises(ValueError, match="does not match"):
        address.validate_viacep_response(payload)


def test_validate_viacep_response_rejects_missing_city():
    address = Address(
        cep_id="01001000",
        street="Praça da Sé",
        neighborhood="Sé",
        city="São Paulo",
        state="SP",
    )
    address.city = ""
    with pytest.raises(ValueError, match="missing city or state"):
        address.validate_viacep_response(stub_viacep_payload())
