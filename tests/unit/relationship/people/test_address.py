import pytest
from pydantic import ValidationError

from src.domain.relationship.entities import Address
from tests.unit.relationship.people.stubs import stub_address


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
