from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    CustomerDTO,
    PersonAddressDTO,
    PersonDTO,
)


class ForStoringData(ABC):
    """Driven port: persistence. The application never sees SQLAlchemy."""

    @abstractmethod
    def create_db_and_tables(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def get_customer(self, customer_id: int) -> CustomerDTO | None:
        pass

    @abstractmethod
    def get_customer_by_cpf(self, cpf: str) -> CustomerDTO | None:
        pass

    @abstractmethod
    def save_customer(self, customer: CustomerDTO) -> CustomerDTO:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> None:
        pass

    @abstractmethod
    def get_person(self, cpf: str) -> PersonDTO | None:
        pass

    @abstractmethod
    def save_person(self, person: PersonDTO) -> PersonDTO:
        pass

    @abstractmethod
    def get_address(self, cep_id: str) -> AddressDTO | None:
        pass

    @abstractmethod
    def save_address(self, address: AddressDTO) -> AddressDTO:
        pass

    @abstractmethod
    def save_person_address(self, person_address: PersonAddressDTO) -> PersonAddressDTO:
        pass

    @abstractmethod
    def save_new_customer_registration(
        self,
        address: AddressDTO,
        person: PersonDTO,
        person_address: PersonAddressDTO,
        customer: CustomerDTO,
    ) -> CustomerDTO:
        pass
