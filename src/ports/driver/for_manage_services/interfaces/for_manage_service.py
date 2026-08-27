from abc import ABC, abstractmethod
from src.ports.driver.for_manage_services.dto.service_dto import ServiceDTO, ServiceCreateDTO, ServiceUpdateDTO


class ForManageService(ABC):
    @abstractmethod
    def create_service(self, service: ServiceCreateDTO) -> ServiceDTO:
        pass

    @abstractmethod
    def update_service(self, service_id: int, service: ServiceUpdateDTO) -> ServiceDTO:
        pass

    @abstractmethod
    def delete_service(self, service_id: int) -> None:
        pass

    @abstractmethod
    def get_service(self, service_id: int) -> ServiceDTO:
        pass