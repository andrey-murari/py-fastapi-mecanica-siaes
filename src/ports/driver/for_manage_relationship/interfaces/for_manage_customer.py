from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto import (
    AddressDTO,
    CustomerCreateDTO,
    CustomerDetailDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
)


class ForManageCustomer(ABC):
    @abstractmethod
    def create_customer(self, customer: CustomerFullCreateDTO) -> CustomerDTO:
        pass

    @abstractmethod
    def create_customer_only_cpf(self, customer: CustomerCreateDTO) -> CustomerDTO:
        pass

    @abstractmethod
    def read_customer(self, customer_id: int) -> CustomerDetailDTO:
        pass

    @abstractmethod
    def find_customer_by_cpf(self, cpf: str) -> CustomerDetailDTO:
        pass

    @abstractmethod
    def update_customer(self, customer_id: int, customer: CustomerUpdateDTO) -> CustomerDTO:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> dict:
        pass

    @abstractmethod
    def get_address_by_cep(self, cep: str) -> AddressDTO:
        pass
