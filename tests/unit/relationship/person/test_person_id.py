import pytest
from pydantic import ValidationError

from src.domain.relationship.entities.contacts import PersonContact
from src.domain.relationship.entities.person import Person, PersonAddress
from src.domain.relationship.value_objects.contact_type import ContactType


def _person(person_id: str) -> Person:
    return Person(
        person_id=person_id,
        complete_name="Andrey Murari",
        user_id="52998224725",
        user_modification_id=1,
    )


def test_accepts_valid_cpf_with_mask():
    assert _person("529.982.247-25").person_id == "52998224725"


def test_accepts_valid_cpf_digits_only():
    assert _person("52998224725").person_id == "52998224725"


def test_rejects_cpf_with_wrong_check_digits():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        _person("123.456.789-12")


def test_rejects_cpf_with_all_digits_equal():
    with pytest.raises(ValidationError, match="all digits equal"):
        _person("777.777.777-77")


def test_accepts_valid_cnpj_with_mask():
    assert _person("11.222.333/0001-81").person_id == "11222333000181"


def test_accepts_valid_cnpj_digits_only():
    assert _person("11222333000181").person_id == "11222333000181"


def test_rejects_cnpj_with_wrong_check_digits():
    with pytest.raises(ValidationError, match="Invalid CNPJ"):
        _person("11.222.333/0001-99")


def test_rejects_cnpj_with_all_digits_equal():
    with pytest.raises(ValidationError, match="all digits equal"):
        _person("11111111111111")


@pytest.mark.parametrize("person_id", ["529982247", "529982247251", "5299822472512"])
def test_rejects_wrong_length(person_id: str):
    with pytest.raises(ValidationError, match="valid CPF .11 digits. or CNPJ .14 digits."):
        _person(person_id)


def test_person_defaults_to_non_customer():
    assert _person("52998224725").flag_customer is False


def test_person_address_reuses_person_id_validation():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        PersonAddress(person_id="123.456.789-12", cep_id="01001000", number="100")
    link = PersonAddress(person_id="529.982.247-25", cep_id="01001-000", number="100")
    assert link.person_id == "52998224725"
    assert link.cep_id == "01001000"


def test_person_contact_reuses_person_id_validation():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        PersonContact(
            person_id="123.456.789-12", contact_type=ContactType.EMAIL, value="a@b.com"
        )
    contact = PersonContact(
        person_id="11.222.333/0001-81",
        contact_type=ContactType.MOBILE,
        value="(11) 98765-4321",
    )
    assert contact.person_id == "11222333000181"
    assert contact.value == "11987654321"
