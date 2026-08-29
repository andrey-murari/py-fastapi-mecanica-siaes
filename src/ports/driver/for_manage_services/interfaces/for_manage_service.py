from abc import ABC, abstractmethod

from src.ports.driver.for_manage_services.dto.service_dto import (
    ServiceCreateDTO,
    ServiceDTO,
    ServiceUpdateDTO,
)


class ForManageService(ABC):
    @abstractmethod
    def create_service(self, service: ServiceCreateDTO) -> ServiceDTO:
        pass

    @abstractmethod
    def read_service(self, service_id: int) -> ServiceDTO:
        pass

    @abstractmethod
    def update_service(self, service_id: int, service: ServiceUpdateDTO) -> ServiceDTO:
        pass

    @abstractmethod
    def delete_service(self, service_id: int) -> dict:
        pass
