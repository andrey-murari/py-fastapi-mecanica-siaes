from typing import override

from pydantic import ValidationError

from src.domain.relationship.application.person_login import create_login_for_person
from src.domain.relationship.entities.contacts import PersonContact
from src.domain.relationship.entities.person import Person
from src.domain.relationship.value_objects.user_type import UserType
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_relationship.dto.person_dto import (
    PersonAddressViewDTO,
    PersonContactCreateDTO,
    PersonContactDTO,
    PersonContactUpdateDTO,
    PersonContactViewDTO,
    PersonCreateDTO,
    PersonDetailDTO,
    PersonDTO,
    PersonUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class PersonUseCases(ForManagePerson):
    """Implements the driver port and depends only on driven ports."""

    def __init__(self, storage: ForStoringData) -> None:
        self._storage = storage

    @override
    def create_person(self, person: PersonCreateDTO) -> PersonDTO:
        try:
            entity = Person(
                person_id=person.person_id,
                complete_name=person.complete_name,
                user_modification_id=person.user_modification_id,
                flag_active=person.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if self._storage.get_person(entity.person_id) is not None:
            raise ValueError("Person already exists")
        account = create_login_for_person(
            self._storage,
            entity.person_id,
            entity.complete_name,
            UserType.USER,
            entity.user_modification_id,
        )
        return self._storage.save_person(
            PersonDTO.model_validate(entity.model_copy(update={"user_id": account.user_id}))
        )

    @override
    def read_person(self, person_id: str) -> PersonDetailDTO:
        person = self._storage.get_person(self._person_id(person_id))
        if person is None:
            raise ValueError("Person not found")
        return PersonDetailDTO(
            **person.model_dump(),
            addresses=[
                PersonAddressViewDTO.model_validate(address)
                for address in self._storage.get_person_addresses(person.person_id)
            ],
            contacts=[
                PersonContactViewDTO.model_validate(contact)
                for contact in self._storage.get_contacts_by_person_id(person.person_id)
            ],
        )

    @override
    def update_person(self, person_id: str, person: PersonUpdateDTO) -> PersonDTO:
        stored = self._storage.get_person(self._person_id(person_id))
        if stored is None:
            raise ValueError("Person not found")
        changes = person.model_dump(exclude_unset=True, exclude_none=True)
        try:
            updated = Person.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        self._ensure_unique_user(updated.user_id, person_id=updated.person_id)
        return self._storage.save_person(PersonDTO.model_validate(updated))

    @override
    def delete_person(self, person_id: str) -> dict:
        stored_id = self._person_id(person_id)
        if self._storage.get_person(stored_id) is None:
            raise ValueError("Person not found")
        if self._storage.get_vehicles_by_person_id(stored_id):
            raise ValueError("Person has vehicles")
        self._storage.delete_person(stored_id)
        return {"ok": True}

    @override
    def create_contact(self, person_id: str, contact: PersonContactCreateDTO) -> PersonContactDTO:
        stored_id = self._require_person(person_id)
        try:
            entity = PersonContact(
                person_id=stored_id,
                contact_type=contact.contact_type,
                value=contact.value,
                flag_preferred=contact.flag_preferred,
                user_modification_id=contact.user_modification_id,
                flag_active=contact.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if entity.flag_preferred:
            self._clear_other_preferred(stored_id, keep_contact_id=None)
        return self._storage.save_contact(PersonContactDTO.model_validate(entity))

    @override
    def list_contacts(self, person_id: str) -> list[PersonContactDTO]:
        return self._storage.get_contacts_by_person_id(self._require_person(person_id))

    @override
    def read_contact(self, person_id: str, contact_id: int) -> PersonContactDTO:
        return self._require_contact(person_id, contact_id)

    @override
    def update_contact(
        self,
        person_id: str,
        contact_id: int,
        contact: PersonContactUpdateDTO,
    ) -> PersonContactDTO:
        stored = self._require_contact(person_id, contact_id)
        changes = contact.model_dump(exclude_unset=True, exclude_none=True)
        try:
            updated = PersonContact.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if updated.flag_preferred:
            self._clear_other_preferred(updated.person_id, keep_contact_id=contact_id)
        return self._storage.save_contact(PersonContactDTO.model_validate(updated))

    @override
    def delete_contact(self, person_id: str, contact_id: int) -> dict:
        self._require_contact(person_id, contact_id)
        self._storage.delete_contact(contact_id)
        return {"ok": True}

    def _ensure_unique_user(self, user_id: str | None, person_id: str | None = None) -> None:
        if user_id is None:
            return
        owner = self._storage.get_person_by_user_id(user_id)
        if owner is not None and owner.person_id != person_id:
            raise ValueError("User already linked to a person")

    def _person_id(self, person_id: str) -> str:
        return Person.validate_person_id(person_id)

    def _require_person(self, person_id: str) -> str:
        stored_id = self._person_id(person_id)
        if self._storage.get_person(stored_id) is None:
            raise ValueError("Person not found")
        return stored_id

    def _require_contact(self, person_id: str, contact_id: int) -> PersonContactDTO:
        stored_id = self._require_person(person_id)
        stored = self._storage.get_contact(contact_id)
        if stored is None or stored.person_id != stored_id:
            raise ValueError("Contact not found")
        return stored

    def _clear_other_preferred(self, person_id: str, keep_contact_id: int | None) -> None:
        for contact in self._storage.get_contacts_by_person_id(person_id):
            if not contact.flag_preferred:
                continue
            if keep_contact_id is not None and contact.contact_id == keep_contact_id:
                continue
            self._storage.save_contact(contact.model_copy(update={"flag_preferred": False}))
