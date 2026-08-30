from fastapi import HTTPException

from src.domain.relationship.value_objects.contact_type import ContactType
from src.ports.driver.for_manage_relationship.dto.person_dto import (
    PersonContactCreateDTO,
    PersonContactDTO,
    PersonContactUpdateDTO,
    PersonCreateDTO,
    PersonDetailDTO,
    PersonDTO,
    PersonUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ui.rest.routers.relationship.person_router import (
    create_contact,
    create_person,
    delete_contact,
    delete_person,
    list_contacts,
    read_contact,
    read_person,
    update_contact,
    update_person,
)

VALID_CPF = "52998224725"
UNKNOWN_CPF = "11144477735"


class _FakeUseCase(ForManagePerson):
    def create_person(self, person: PersonCreateDTO) -> PersonDTO:
        if person.person_id == UNKNOWN_CPF:
            raise ValueError("Person already exists")
        if person.person_id == "12345678912":
            raise ValueError("Invalid CPF")
        return PersonDTO(
            person_id=person.person_id,
            complete_name=person.complete_name,
            user_id=person.person_id,
            user_modification_id=person.user_modification_id,
        )

    def read_person(self, person_id: str) -> PersonDetailDTO:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Person not found")
        if person_id == "123":
            raise ValueError("Invalid CPF")
        return PersonDetailDTO(
            person_id=person_id,
            complete_name="Andrey Murari",
            user_id=person_id,
            user_modification_id=1,
        )

    def update_person(self, person_id: str, person: PersonUpdateDTO) -> PersonDTO:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Person not found")
        if person.complete_name == "Andrey 2":
            raise ValueError("Complete name must not contain numbers")
        return PersonDTO(
            person_id=person_id,
            complete_name=person.complete_name or "Andrey Murari",
            user_id=person_id,
            user_modification_id=1,
        )

    def delete_person(self, person_id: str) -> dict:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Person not found")
        if person_id == VALID_CPF:
            raise ValueError("Person has vehicles")
        return {"ok": True}

    def create_contact(self, person_id: str, contact: PersonContactCreateDTO) -> PersonContactDTO:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Person not found")
        if contact.value == "bad":
            raise ValueError("Invalid email")
        return PersonContactDTO(
            contact_id=1,
            person_id=person_id,
            contact_type=contact.contact_type,
            value=contact.value,
            flag_preferred=contact.flag_preferred,
        )

    def list_contacts(self, person_id: str) -> list[PersonContactDTO]:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Person not found")
        return [
            PersonContactDTO(
                contact_id=1,
                person_id=person_id,
                contact_type=ContactType.MOBILE,
                value="11987654321",
            )
        ]

    def read_contact(self, person_id: str, contact_id: int) -> PersonContactDTO:
        if contact_id == 99:
            raise ValueError("Contact not found")
        return PersonContactDTO(
            contact_id=contact_id,
            person_id=person_id,
            contact_type=ContactType.MOBILE,
            value="11987654321",
        )

    def update_contact(
        self,
        person_id: str,
        contact_id: int,
        contact: PersonContactUpdateDTO,
    ) -> PersonContactDTO:
        if contact_id == 99:
            raise ValueError("Contact not found")
        if contact.value == "bad":
            raise ValueError("Invalid phone")
        return PersonContactDTO(
            contact_id=contact_id,
            person_id=person_id,
            contact_type=ContactType.MOBILE,
            value=contact.value or "11987654321",
        )

    def delete_contact(self, person_id: str, contact_id: int) -> dict:
        if contact_id == 99:
            raise ValueError("Contact not found")
        return {"ok": True}


def _person_payload() -> PersonCreateDTO:
    return PersonCreateDTO(person_id=VALID_CPF, complete_name="Andrey Murari")


def _contact_payload() -> PersonContactCreateDTO:
    return PersonContactCreateDTO(contact_type=ContactType.MOBILE, value="11987654321")


def test_router_create_delegates_to_port():
    result = create_person(_person_payload(), use_case=_FakeUseCase())
    assert result.person_id == VALID_CPF
    assert result.complete_name == "Andrey Murari"


def test_router_create_maps_value_error_to_400():
    try:
        create_person(
            PersonCreateDTO(person_id=UNKNOWN_CPF, complete_name="Maria Silva"),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Person already exists"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_not_found_to_404():
    try:
        read_person(UNKNOWN_CPF, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Person not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_invalid_person_id_to_400():
    try:
        read_person("123", use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Invalid CPF"
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_maps_validation_to_400():
    try:
        update_person(
            VALID_CPF,
            PersonUpdateDTO(complete_name="Andrey 2"),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Complete name must not contain numbers"
    else:
        raise AssertionError("expected HTTPException")


def test_router_delete_maps_vehicle_link_to_400():
    try:
        delete_person(VALID_CPF, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Person has vehicles"
    else:
        raise AssertionError("expected HTTPException")


def test_router_create_contact_delegates_to_port():
    result = create_contact(VALID_CPF, _contact_payload(), use_case=_FakeUseCase())
    assert result.contact_id == 1
    assert result.value == "11987654321"


def test_router_create_contact_maps_person_not_found_to_404():
    try:
        create_contact(UNKNOWN_CPF, _contact_payload(), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Person not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_list_contacts_delegates_to_port():
    result = list_contacts(VALID_CPF, use_case=_FakeUseCase())
    assert len(result) == 1
    assert result[0].contact_type == ContactType.MOBILE


def test_router_read_contact_maps_not_found_to_404():
    try:
        read_contact(VALID_CPF, 99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Contact not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_contact_maps_validation_to_400():
    try:
        update_contact(
            VALID_CPF,
            1,
            PersonContactUpdateDTO(value="bad"),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Invalid phone"
    else:
        raise AssertionError("expected HTTPException")


def test_router_delete_contact_maps_not_found_to_404():
    try:
        delete_contact(VALID_CPF, 99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Contact not found"
    else:
        raise AssertionError("expected HTTPException")
