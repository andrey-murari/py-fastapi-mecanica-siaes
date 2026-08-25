import pytest
from pydantic import ValidationError

from src.domain.relationship.entities.customer import Customer
from src.domain.relationship.entities.person import Person, PersonAddress


def _person(cpf: str) -> Person:
    return Person(
        cpf=cpf,
        complete_name="Andrey Murari",
        user_id=1,
        user_modification_id=1,
    )


def test_accepts_valid_cpf_with_mask():
    person = _person("529.982.247-25")
    assert person.cpf == "52998224725"


def test_accepts_valid_cpf_digits_only():
    person = _person("52998224725")
    assert person.cpf == "52998224725"


def test_rejects_cpf_with_wrong_check_digits():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        _person("123.456.789-12")


def test_rejects_cpf_with_all_digits_equal():
    with pytest.raises(ValidationError, match="all digits equal"):
        _person("777.777.777-77")


def test_customer_reuses_person_cpf_validation():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        Customer(cpf="123.456.789-12")
    assert Customer(cpf="529.982.247-25").cpf == "52998224725"


def test_person_address_reuses_person_cpf_validation():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        PersonAddress(cpf="123.456.789-12", cep_id="01001000", number="100")
    link = PersonAddress(cpf="529.982.247-25", cep_id="01001-000", number="100")
    assert link.cpf == "52998224725"
    assert link.cep_id == "01001000"
