import pytest
from pydantic import ValidationError

from src.domain.customers_and_services.relationship.entities import People
from tests.unit.relationship.people.stubs import stub_person


def test_create_person():
    person = stub_person()
    assert person.cpf == "12345678901"
    assert person.complete_name == "Andrey Murari"
    assert person.cep_id == 35052130


def test_people_rejects_digits_in_complete_name():
    with pytest.raises(ValidationError, match="must not contain numbers"):
        People(
            cpf="12345678901",
            complete_name="Andrey123",
            cep_id=35052130,
            user_id=1,
            user_modification_id=1,
        )


def test_people_accepts_name_without_digits():
    person = People(
        cpf="12345678901",
        complete_name="andrey",
        cep_id=5040000,
        user_id=1,
        user_modification_id=2,
    )
    assert person.complete_name == "andrey"
