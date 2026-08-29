from datetime import datetime

import pytest

from src.domain.relationship.application.person_use_cases import PersonUseCases
from src.domain.relationship.value_objects.contact_type import ContactType
from src.ports.driver.for_manage_relationship.dto import (
    CustomerDTO,
    PersonAddressDTO,
    PersonContactCreateDTO,
    PersonContactUpdateDTO,
    PersonCreateDTO,
    PersonUpdateDTO,
)
from tests.unit.fakes.in_memory_storage import InMemoryStorage

VALID_CPF = "52998224725"
OTHER_CPF = "11144477735"


def _use_cases() -> tuple[PersonUseCases, InMemoryStorage]:
    storage = InMemoryStorage()
    return PersonUseCases(storage=storage), storage


def _payload(**overrides) -> PersonCreateDTO:
    payload = {
        "cpf": VALID_CPF,
        "complete_name": "Andrey Murari",
    }
    payload.update(overrides)
    return PersonCreateDTO(**payload)


def _contact(**overrides) -> PersonContactCreateDTO:
    payload = {
        "contact_type": ContactType.MOBILE,
        "value": "11987654321",
    }
    payload.update(overrides)
    return PersonContactCreateDTO(**payload)


def test_create_person_persists():
    use_cases, storage = _use_cases()

    created = use_cases.create_person(_payload())

    assert created.cpf == VALID_CPF
    assert created.complete_name == "Andrey Murari"
    assert created.user_id == 1
    assert created.flag_active is True
    assert storage.get_person(VALID_CPF) is not None


def test_create_person_normalizes_masked_cpf():
    use_cases, _ = _use_cases()

    created = use_cases.create_person(_payload(cpf="529.982.247-25"))

    assert created.cpf == VALID_CPF


def test_create_person_rejects_duplicate_cpf():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    with pytest.raises(ValueError, match="Person already exists"):
        use_cases.create_person(_payload())


def test_create_person_rejects_invalid_cpf():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Invalid CPF"):
        use_cases.create_person(_payload(cpf="12345678912"))


def test_create_person_rejects_name_with_digits():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Complete name must not contain numbers"):
        use_cases.create_person(_payload(complete_name="Andrey 2"))


def test_read_person_includes_addresses_and_contacts():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    storage.save_person_address(
        PersonAddressDTO(cpf=VALID_CPF, cep_id="01001000", number="100", complement="apto 1")
    )
    use_cases.create_contact(VALID_CPF, _contact())

    detail = use_cases.read_person(VALID_CPF)

    assert detail.cpf == VALID_CPF
    assert len(detail.addresses) == 1
    assert detail.addresses[0].cep_id == "01001000"
    assert detail.addresses[0].number == "100"
    assert "cpf" not in detail.addresses[0].model_dump()
    assert len(detail.contacts) == 1
    assert detail.contacts[0].value == "11987654321"
    assert "cpf" not in detail.contacts[0].model_dump()


def test_read_person_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Person not found"):
        use_cases.read_person(VALID_CPF)


def test_read_person_rejects_invalid_cpf():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Invalid CPF"):
        use_cases.read_person("12345678912")


def test_update_person_changes_name():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    updated = use_cases.update_person(VALID_CPF, PersonUpdateDTO(complete_name="Maria Silva"))

    assert updated.complete_name == "Maria Silva"
    assert updated.cpf == VALID_CPF


def test_update_person_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Person not found"):
        use_cases.update_person(VALID_CPF, PersonUpdateDTO(complete_name="Maria Silva"))


def test_delete_person_removes_it_and_contacts():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    created_contact = use_cases.create_contact(VALID_CPF, _contact())

    assert use_cases.delete_person(VALID_CPF) == {"ok": True}
    assert storage.get_person(VALID_CPF) is None
    assert storage.get_contact(created_contact.contact_id) is None


def test_delete_person_rejects_when_customer_exists():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    storage.save_customer(CustomerDTO(cpf=VALID_CPF, insertion_date=datetime.now()))

    with pytest.raises(ValueError, match="Person has a customer"):
        use_cases.delete_person(VALID_CPF)


def test_delete_person_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Person not found"):
        use_cases.delete_person(VALID_CPF)


def test_create_contact_requires_person():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Person not found"):
        use_cases.create_contact(VALID_CPF, _contact())


def test_create_contact_normalizes_phone():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    created = use_cases.create_contact(
        VALID_CPF,
        _contact(value="(11) 98765-4321"),
    )

    assert created.contact_id == 1
    assert created.cpf == VALID_CPF
    assert created.contact_type == ContactType.MOBILE
    assert created.value == "11987654321"


def test_create_contact_normalizes_email():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    created = use_cases.create_contact(
        VALID_CPF,
        _contact(contact_type=ContactType.EMAIL, value="Andrey@Example.COM"),
    )

    assert created.value == "andrey@example.com"


def test_create_contact_rejects_invalid_email():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    with pytest.raises(ValueError, match="Invalid email"):
        use_cases.create_contact(
            VALID_CPF,
            _contact(contact_type=ContactType.EMAIL, value="not-an-email"),
        )


def test_create_contact_rejects_invalid_phone():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    with pytest.raises(ValueError, match="Invalid phone"):
        use_cases.create_contact(VALID_CPF, _contact(value="123"))


def test_create_preferred_contact_clears_previous():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    first = use_cases.create_contact(VALID_CPF, _contact(flag_preferred=True))
    second = use_cases.create_contact(
        VALID_CPF,
        _contact(contact_type=ContactType.EMAIL, value="a@b.com", flag_preferred=True),
    )

    assert storage.get_contact(first.contact_id).flag_preferred is False
    assert second.flag_preferred is True


def test_list_contacts():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())
    use_cases.create_contact(VALID_CPF, _contact())
    use_cases.create_contact(
        VALID_CPF,
        _contact(contact_type=ContactType.EMAIL, value="a@b.com"),
    )

    contacts = use_cases.list_contacts(VALID_CPF)

    assert len(contacts) == 2


def test_read_contact_not_found_for_other_person():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())
    use_cases.create_person(_payload(cpf=OTHER_CPF, complete_name="Maria Silva"))
    created = use_cases.create_contact(VALID_CPF, _contact())

    with pytest.raises(ValueError, match="Contact not found"):
        use_cases.read_contact(OTHER_CPF, created.contact_id)


def test_update_contact_changes_value():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())
    created = use_cases.create_contact(VALID_CPF, _contact())

    updated = use_cases.update_contact(
        VALID_CPF,
        created.contact_id,
        PersonContactUpdateDTO(value="11911112222"),
    )

    assert updated.value == "11911112222"


def test_delete_contact():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    created = use_cases.create_contact(VALID_CPF, _contact())

    assert use_cases.delete_contact(VALID_CPF, created.contact_id) == {"ok": True}
    assert storage.get_contact(created.contact_id) is None
