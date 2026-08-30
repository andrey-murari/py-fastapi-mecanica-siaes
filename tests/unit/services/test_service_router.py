from decimal import Decimal

from fastapi import HTTPException

from src.ports.driver.for_manage_services.dto.service_dto import (
    ServiceCreateDTO,
    ServiceDTO,
    ServiceUpdateDTO,
)
from src.ports.driver.for_manage_services.interfaces.for_manage_service import ForManageService
from src.ui.rest.routers.services.service_router import (
    create_service,
    delete_service,
    read_service,
    update_service,
)


class _FakeUseCase(ForManageService):
    def create_service(self, service: ServiceCreateDTO) -> ServiceDTO:
        if service.price < 0:
            raise ValueError("Input should be greater than or equal to 0")
        return ServiceDTO(service_id=1, description=service.description, price=service.price)

    def read_service(self, service_id: int) -> ServiceDTO:
        if service_id == 99:
            raise ValueError("Service not found")
        return ServiceDTO(
            service_id=service_id,
            description="Troca de oleo",
            price=Decimal("150.00"),
        )

    def update_service(self, service_id: int, service: ServiceUpdateDTO) -> ServiceDTO:
        if service_id == 99:
            raise ValueError("Service not found")
        if service.price is not None and service.price < 0:
            raise ValueError("Input should be greater than or equal to 0")
        return ServiceDTO(
            service_id=service_id,
            description=service.description or "Troca de oleo",
            price=service.price or Decimal("150.00"),
        )

    def delete_service(self, service_id: int) -> dict:
        if service_id == 99:
            raise ValueError("Service not found")
        return {"ok": True}


def test_router_create_delegates_to_port():
    result = create_service(
        ServiceCreateDTO(description="Troca de oleo", price=Decimal("150.00")),
        use_case=_FakeUseCase(),
    )

    assert result.service_id == 1
    assert result.price == Decimal("150.00")


def test_router_create_maps_value_error_to_400():
    try:
        create_service(
            ServiceCreateDTO(description="Troca de oleo", price=Decimal("-1")),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_value_error_to_404():
    try:
        read_service(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Service not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_maps_missing_service_to_404():
    try:
        update_service(99, ServiceUpdateDTO(price=Decimal("10")), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_maps_invalid_price_to_400():
    try:
        update_service(1, ServiceUpdateDTO(price=Decimal("-10")), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("expected HTTPException")


def test_router_delete_maps_value_error_to_404():
    try:
        delete_service(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("expected HTTPException")
