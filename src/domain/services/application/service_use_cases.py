from src.ports.driving.for_storing_data.for_storing_data import ForStoringData
from src.ports.driver.for_manage_services.interfaces.for_manage_service import ForManageService
from src.ports.driver.for_manage_services.dto.service_dto import ServiceDTO, ServiceCreateDTO, ServiceUpdateDTO
from typing import override


class ServiceUseCases(ForManageService):
    def __init__(self, storage: ForStoringData) -> None:
        self.storage = storage

    @override
    def create_service(self, service: ServiceCreateDTO) -> ServiceDTO:
        pass

    @override
    def update_service(self, service_id: int, service: ServiceUpdateDTO) -> ServiceDTO:
        pass

    @override
    def delete_service(self, service_id: int) -> None:
        pass

    @override
    def get_service(self, service_id: int) -> ServiceDTO:
        pass