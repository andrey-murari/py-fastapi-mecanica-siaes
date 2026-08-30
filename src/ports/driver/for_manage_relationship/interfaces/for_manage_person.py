from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto.person_dto import (
    PersonContactCreateDTO,
    PersonContactDTO,
    PersonContactUpdateDTO,
    PersonCreateDTO,
    PersonDetailDTO,
    PersonDTO,
    PersonUpdateDTO,
)


class ForManagePerson(ABC):
    @abstractmethod
    def create_person(self, person: PersonCreateDTO) -> PersonDTO:
        pass

    @abstractmethod
    def read_person(self, person_id: str) -> PersonDetailDTO:
        pass

    @abstractmethod
    def update_person(self, person_id: str, person: PersonUpdateDTO) -> PersonDTO:
        pass

    @abstractmethod
    def delete_person(self, person_id: str) -> dict:
        pass

    @abstractmethod
    def create_contact(self, person_id: str, contact: PersonContactCreateDTO) -> PersonContactDTO:
        pass

    @abstractmethod
    def list_contacts(self, person_id: str) -> list[PersonContactDTO]:
        pass

    @abstractmethod
    def read_contact(self, person_id: str, contact_id: int) -> PersonContactDTO:
        pass

    @abstractmethod
    def update_contact(
        self,
        person_id: str,
        contact_id: int,
        contact: PersonContactUpdateDTO,
    ) -> PersonContactDTO:
        pass

    @abstractmethod
    def delete_contact(self, person_id: str, contact_id: int) -> dict:
        pass
