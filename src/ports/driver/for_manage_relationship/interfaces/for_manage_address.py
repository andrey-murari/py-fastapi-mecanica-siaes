from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto.address_dto import AddressDTO

class ForManageAddress(ABC):
    @abstractmethod
    def create_address(self, address: dict) -> AddressDTO:
        pass

    @abstractmethod
    def read_address(self, address_id: int) -> AddressDTO:
        pass

    @abstractmethod
    def update_address(self, address_id: int, address: dict) -> AddressDTO:
        pass

    @abstractmethod
    def delete_address(self, address_id: int) -> None:
        pass