from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto.person_dto import PersonCreateDTO, PersonDTO, PersonUpdateDTO


class ForManagePerson(ABC):
    @abstractmethod
    def create_person(self, person: PersonCreateDTO) -> PersonDTO:
        pass

    @abstractmethod
    def read_person(self, person_id: int) -> PersonDTO:
        pass

    @abstractmethod
    def update_person(self, person_id: int, person: PersonUpdateDTO) -> PersonDTO:
        pass

    @abstractmethod
    def delete_person(self, person_id: int) -> dict:
        pass
