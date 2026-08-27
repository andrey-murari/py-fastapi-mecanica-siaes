from fastapi import HTTPException

from src.domain.relationship.value_objects.fuel_type import FuelType
from src.ports.driver.for_manage_relationship.dto.vehicle_dto import (
    VehicleCreateDTO,
    VehicleCustomerCreateDTO,
    VehicleDetailDTO,
    VehicleDTO,
    VehicleUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ui.rest.routers.relationship.vehicle_router import (
    create_vehicle,
    delete_vehicle,
    find_vehicles_by_customer_cpf,
    read_vehicle,
    update_vehicle,
)


class _FakeUseCase(ForManageVehicle):
    def create_vehicle(self, vehicle: VehicleCreateDTO) -> VehicleDTO:
        if vehicle.customer_vehicle.customer_id == 99:
            raise ValueError("Customer not found")
        return VehicleDTO(
            vehicle_id=1,
            model=vehicle.model,
            brand=vehicle.brand,
            manufacture_year=vehicle.manufacture_year,
            model_year=vehicle.model_year,
            engine=vehicle.engine,
            fuel_type=vehicle.fuel_type,
        )

    def read_vehicle(self, vehicle_id: int) -> VehicleDetailDTO:
        if vehicle_id == 99:
            raise ValueError("Vehicle not found")
        return VehicleDetailDTO(
            vehicle_id=vehicle_id,
            model="Civic",
            brand="Honda",
            manufacture_year="2020",
            model_year="2021",
            engine="2.0",
            fuel_type=FuelType.GASOLINE,
        )

    def update_vehicle(self, vehicle_id: int, vehicle: VehicleUpdateDTO) -> VehicleDTO:
        if vehicle_id == 99:
            raise ValueError("Vehicle not found")
        if vehicle.plate == "DUP1A23":
            raise ValueError("Plate already exists")
        return VehicleDTO(
            vehicle_id=vehicle_id,
            model=vehicle.model or "Civic",
            brand="Honda",
            manufacture_year="2020",
            model_year="2021",
            engine="2.0",
            fuel_type=FuelType.GASOLINE,
        )

    def delete_vehicle(self, vehicle_id: int) -> dict:
        if vehicle_id == 99:
            raise ValueError("Vehicle not found")
        return {"ok": True}

    def find_vehicles_by_customer_cpf(self, cpf: str) -> list[VehicleDetailDTO]:
        if cpf == "11144477735":
            raise ValueError("Customer not found")
        return [
            VehicleDetailDTO(
                vehicle_id=1,
                model="Civic",
                brand="Honda",
                manufacture_year="2020",
                model_year="2021",
                engine="2.0",
                fuel_type=FuelType.GASOLINE,
            )
        ]


def _payload() -> VehicleCreateDTO:
    return VehicleCreateDTO(
        model="Civic",
        brand="Honda",
        manufacture_year="2020",
        model_year="2021",
        engine="2.0",
        fuel_type=FuelType.GASOLINE,
        customer_vehicle=VehicleCustomerCreateDTO(
            customer_id=1,
            plate="ABC1D23",
            color="Prata",
        ),
    )


def test_router_create_delegates_to_port():
    result = create_vehicle(_payload(), use_case=_FakeUseCase())
    assert result.vehicle_id == 1
    assert result.model == "Civic"


def test_router_create_maps_value_error_to_400():
    payload = _payload()
    payload.customer_vehicle.customer_id = 99
    try:
        create_vehicle(payload, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_value_error_to_404():
    try:
        read_vehicle(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Vehicle not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_maps_duplicate_plate_to_400():
    try:
        update_vehicle(1, VehicleUpdateDTO(plate="DUP1A23"), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Plate already exists"
    else:
        raise AssertionError("expected HTTPException")


def test_router_delete_maps_value_error_to_404():
    try:
        delete_vehicle(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Vehicle not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_find_by_cpf_delegates_to_port():
    result = find_vehicles_by_customer_cpf("52998224725", use_case=_FakeUseCase())
    assert len(result) == 1
    assert result[0].model == "Civic"


def test_router_find_by_cpf_maps_customer_not_found_to_404():
    try:
        find_vehicles_by_customer_cpf("11144477735", use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")
