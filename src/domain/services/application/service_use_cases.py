from typing import override

from pydantic import ValidationError

from src.domain.services.entities.service import Service
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_services.dto.service_dto import (
    ServiceCreateDTO,
    ServiceDTO,
    ServiceUpdateDTO,
)
from src.ports.driver.for_manage_services.interfaces.for_manage_service import ForManageService
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class ServiceUseCases(ForManageService):
    """Implements the driver port and depends only on driven ports."""

    def __init__(self, storage: ForStoringData) -> None:
        self._storage = storage

    @override
    def create_service(self, service: ServiceCreateDTO) -> ServiceDTO:
        try:
            entity = Service(
                description=service.description,
                price=service.price,
                average_duration_minutes=service.average_duration_minutes,
                user_modification_id=service.user_modification_id,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        return self._storage.save_service(ServiceDTO.model_validate(entity))

    @override
    def read_service(self, service_id: int) -> ServiceDTO:
        service = self._storage.get_service(service_id)
        if service is None:
            raise ValueError("Service not found")
        return service

    @override
    def update_service(self, service_id: int, service: ServiceUpdateDTO) -> ServiceDTO:
        stored = self._storage.get_service(service_id)
        if stored is None:
            raise ValueError("Service not found")
        changes = service.model_dump(exclude_unset=True, exclude_none=True)
        try:
            updated = Service.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        return self._storage.save_service(ServiceDTO.model_validate(updated))

    @override
    def delete_service(self, service_id: int) -> dict:
        if self._storage.get_service(service_id) is None:
            raise ValueError("Service not found")
        self._storage.delete_service(service_id)
        return {"ok": True}
