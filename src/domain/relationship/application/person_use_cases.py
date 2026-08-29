from typing import override

from pydantic import ValidationError

from src.domain.relationship.entities.contacts import PersonContact
from src.domain.relationship.entities.person import Person
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
                cpf=person.cpf,
                complete_name=person.complete_name,
                user_id=person.user_id,
                user_modification_id=person.user_modification_id,
                flag_active=person.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if self._storage.get_person(entity.cpf) is not None:
            raise ValueError("Person already exists")
        return self._storage.save_person(PersonDTO.model_validate(entity))

    @override
    def read_person(self, cpf: str) -> PersonDetailDTO:
        person = self._storage.get_person(self._cpf(cpf))
        if person is None:
            raise ValueError("Person not found")
        return PersonDetailDTO(
            **person.model_dump(),
            addresses=[
                PersonAddressViewDTO.model_validate(address)
                for address in self._storage.get_person_addresses(person.cpf)
            ],
            contacts=[
                PersonContactViewDTO.model_validate(contact)
                for contact in self._storage.get_contacts_by_cpf(person.cpf)
            ],
        )

    @override
    def update_person(self, cpf: str, person: PersonUpdateDTO) -> PersonDTO:
        stored = self._storage.get_person(self._cpf(cpf))
        if stored is None:
            raise ValueError("Person not found")
        changes = person.model_dump(exclude_unset=True, exclude_none=True)
        try:
            updated = Person.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        return self._storage.save_person(PersonDTO.model_validate(updated))

    @override
    def delete_person(self, cpf: str) -> dict:
        person_cpf = self._cpf(cpf)
        if self._storage.get_person(person_cpf) is None:
            raise ValueError("Person not found")
        if self._storage.get_customer_by_cpf(person_cpf) is not None:
            raise ValueError("Person has a customer")
        self._storage.delete_person(person_cpf)
        return {"ok": True}

    @override
    def create_contact(self, cpf: str, contact: PersonContactCreateDTO) -> PersonContactDTO:
        person_cpf = self._require_person(cpf)
        try:
            entity = PersonContact(
                cpf=person_cpf,
                contact_type=contact.contact_type,
                value=contact.value,
                flag_preferred=contact.flag_preferred,
                user_modification_id=contact.user_modification_id,
                flag_active=contact.flag_active,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if entity.flag_preferred:
            self._clear_other_preferred(person_cpf, keep_contact_id=None)
        return self._storage.save_contact(PersonContactDTO.model_validate(entity))

    @override
    def list_contacts(self, cpf: str) -> list[PersonContactDTO]:
        return self._storage.get_contacts_by_cpf(self._require_person(cpf))

    @override
    def read_contact(self, cpf: str, contact_id: int) -> PersonContactDTO:
        return self._require_contact(cpf, contact_id)

    @override
    def update_contact(
        self,
        cpf: str,
        contact_id: int,
        contact: PersonContactUpdateDTO,
    ) -> PersonContactDTO:
        stored = self._require_contact(cpf, contact_id)
        changes = contact.model_dump(exclude_unset=True, exclude_none=True)
        try:
            updated = PersonContact.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if updated.flag_preferred:
            self._clear_other_preferred(updated.cpf, keep_contact_id=contact_id)
        return self._storage.save_contact(PersonContactDTO.model_validate(updated))

    @override
    def delete_contact(self, cpf: str, contact_id: int) -> dict:
        self._require_contact(cpf, contact_id)
        self._storage.delete_contact(contact_id)
        return {"ok": True}

    def _cpf(self, cpf: str) -> str:
        return Person.validate_cpf(cpf)

    def _require_person(self, cpf: str) -> str:
        person_cpf = self._cpf(cpf)
        if self._storage.get_person(person_cpf) is None:
            raise ValueError("Person not found")
        return person_cpf

    def _require_contact(self, cpf: str, contact_id: int) -> PersonContactDTO:
        person_cpf = self._require_person(cpf)
        stored = self._storage.get_contact(contact_id)
        if stored is None or stored.cpf != person_cpf:
            raise ValueError("Contact not found")
        return stored

    def _clear_other_preferred(self, cpf: str, keep_contact_id: int | None) -> None:
        for contact in self._storage.get_contacts_by_cpf(cpf):
            if not contact.flag_preferred:
                continue
            if keep_contact_id is not None and contact.contact_id == keep_contact_id:
                continue
            self._storage.save_contact(contact.model_copy(update={"flag_preferred": False}))
