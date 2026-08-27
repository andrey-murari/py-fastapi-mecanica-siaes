from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto import AddressDTO

class ForGetAddress(ABC):
    @abstractmethod
    def get_address_by_cep(self, cep: str) -> AddressDTO:
        pass