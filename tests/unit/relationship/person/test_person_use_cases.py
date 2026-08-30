import pytest

from src.domain.relationship.application.person_use_cases import PersonUseCases
from src.domain.relationship.value_objects.contact_type import ContactType
from src.domain.relationship.value_objects.fuel_type import FuelType
from src.ports.driver.for_manage_relationship.dto import (
    PersonAddressDTO,
    PersonContactCreateDTO,
    PersonContactUpdateDTO,
    PersonCreateDTO,
    PersonUpdateDTO,
    VehicleDTO,
)
from tests.unit.fakes.in_memory_storage import InMemoryStorage

VALID_CPF = "52998224725"
OTHER_CPF = "11144477735"
VALID_CNPJ = "11222333000181"


def _use_cases() -> tuple[PersonUseCases, InMemoryStorage]:
    storage = InMemoryStorage()
    return PersonUseCases(storage=storage), storage


def _payload(**overrides) -> PersonCreateDTO:
    payload = {
        "person_id": VALID_CPF,
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

    assert created.person_id == VALID_CPF
    assert created.complete_name == "Andrey Murari"
    assert created.user_id == VALID_CPF
    assert storage.get_user(VALID_CPF).login == VALID_CPF
    assert storage.get_user(VALID_CPF).password == "AM4725"
    assert created.flag_active is True
    assert created.flag_customer is False
    assert storage.get_person(VALID_CPF) is not None


def test_create_person_normalizes_masked_cpf():
    use_cases, _ = _use_cases()

    created = use_cases.create_person(_payload(person_id="529.982.247-25"))

    assert created.person_id == VALID_CPF


def test_create_person_accepts_cnpj():
    use_cases, _ = _use_cases()

    created = use_cases.create_person(_payload(person_id="11.222.333/0001-81"))

    assert created.person_id == VALID_CNPJ


def test_create_person_rejects_duplicate_cpf():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    payload = _payload()
    with pytest.raises(ValueError, match="Person already exists"):
        use_cases.create_person(payload)


def test_create_person_rejects_invalid_cpf():
    use_cases, _ = _use_cases()

    payload = _payload(person_id="12345678912")
    with pytest.raises(ValueError, match="Invalid CPF"):
        use_cases.create_person(payload)


def test_create_person_rejects_name_with_digits():
    use_cases, _ = _use_cases()

    payload = _payload(complete_name="Andrey 2")
    with pytest.raises(ValueError, match="Complete name must not contain numbers"):
        use_cases.create_person(payload)


def test_read_person_includes_addresses_and_contacts():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    storage.save_person_address(
        PersonAddressDTO(
            person_id=VALID_CPF, cep_id="01001000", number="100", complement="apto 1"
        )
    )
    use_cases.create_contact(VALID_CPF, _contact())

    detail = use_cases.read_person(VALID_CPF)

    assert detail.person_id == VALID_CPF
    assert len(detail.addresses) == 1
    assert detail.addresses[0].cep_id == "01001000"
    assert detail.addresses[0].number == "100"
    assert "person_id" not in detail.addresses[0].model_dump()
    assert len(detail.contacts) == 1
    assert detail.contacts[0].value == "11987654321"
    assert "person_id" not in detail.contacts[0].model_dump()


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
    assert updated.person_id == VALID_CPF


def test_update_person_rejects_user_already_linked():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())
    use_cases.create_person(_payload(person_id=OTHER_CPF, complete_name="Maria Silva"))

    payload = PersonUpdateDTO(user_id=VALID_CPF)
    with pytest.raises(ValueError, match="User already linked to a person"):
        use_cases.update_person(OTHER_CPF, payload)


def test_update_person_not_found():
    use_cases, _ = _use_cases()

    payload = PersonUpdateDTO(complete_name="Maria Silva")
    with pytest.raises(ValueError, match="Person not found"):
        use_cases.update_person(VALID_CPF, payload)


def test_delete_person_removes_it_and_contacts():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    created_contact = use_cases.create_contact(VALID_CPF, _contact())

    assert use_cases.delete_person(VALID_CPF) == {"ok": True}
    assert storage.get_person(VALID_CPF) is None
    assert storage.get_contact(created_contact.contact_id) is None


def test_delete_person_rejects_when_person_has_vehicles():
    use_cases, storage = _use_cases()
    use_cases.create_person(_payload())
    storage.save_vehicle(
        VehicleDTO(
            person_id=VALID_CPF,
            model="Civic",
            brand="Honda",
            manufacture_year="2020",
            model_year="2021",
            engine="2.0",
            fuel_type=FuelType.GASOLINE,
            plate="ABC1D23",
            color="Prata",
        )
    )

    with pytest.raises(ValueError, match="Person has vehicles"):
        use_cases.delete_person(VALID_CPF)


def test_delete_person_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Person not found"):
        use_cases.delete_person(VALID_CPF)


def test_create_contact_requires_person():
    use_cases, _ = _use_cases()

    contact = _contact()
    with pytest.raises(ValueError, match="Person not found"):
        use_cases.create_contact(VALID_CPF, contact)


def test_create_contact_normalizes_phone():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    created = use_cases.create_contact(
        VALID_CPF,
        _contact(value="(11) 98765-4321"),
    )

    assert created.contact_id == 1
    assert created.person_id == VALID_CPF
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

    contact = _contact(contact_type=ContactType.EMAIL, value="not-an-email")
    with pytest.raises(ValueError, match="Invalid email"):
        use_cases.create_contact(VALID_CPF, contact)


def test_create_contact_rejects_invalid_phone():
    use_cases, _ = _use_cases()
    use_cases.create_person(_payload())

    contact = _contact(value="123")
    with pytest.raises(ValueError, match="Invalid phone"):
        use_cases.create_contact(VALID_CPF, contact)


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
    use_cases.create_person(_payload(person_id=OTHER_CPF, complete_name="Maria Silva"))
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
