from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto import (
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
    def read_customer(self, person_id: str) -> CustomerDetailDTO:
        pass

    @abstractmethod
    def update_customer(self, person_id: str, customer: CustomerUpdateDTO) -> CustomerDTO:
        pass

    @abstractmethod
    def delete_customer(self, person_id: str) -> dict:
        pass
