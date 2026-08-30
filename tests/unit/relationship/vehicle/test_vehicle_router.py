from fastapi import HTTPException

from src.domain.relationship.value_objects.fuel_type import FuelType
from src.ports.driver.for_manage_relationship.dto.vehicle_dto import (
    VehicleCreateDTO,
    VehicleDTO,
    VehicleUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ui.rest.routers.relationship.vehicle_router import (
    create_vehicle,
    delete_vehicle,
    find_vehicles_by_person_id,
    read_vehicle,
    update_vehicle,
)

VALID_CPF = "52998224725"
NOT_A_CUSTOMER_CPF = "11144477735"


def _vehicle(vehicle_id: int = 1, **overrides) -> VehicleDTO:
    payload = {
        "vehicle_id": vehicle_id,
        "person_id": VALID_CPF,
        "model": "Civic",
        "brand": "Honda",
        "manufacture_year": "2020",
        "model_year": "2021",
        "engine": "2.0",
        "fuel_type": FuelType.GASOLINE,
        "plate": "ABC1D23",
        "color": "Prata",
    }
    payload.update(overrides)
    return VehicleDTO(**payload)


class _FakeUseCase(ForManageVehicle):
    def create_vehicle(self, vehicle: VehicleCreateDTO) -> VehicleDTO:
        if vehicle.person_id == NOT_A_CUSTOMER_CPF:
            raise ValueError("Person is not a customer")
        return _vehicle(person_id=vehicle.person_id, model=vehicle.model, plate=vehicle.plate)

    def read_vehicle(self, vehicle_id: int) -> VehicleDTO:
        if vehicle_id == 99:
            raise ValueError("Vehicle not found")
        return _vehicle(vehicle_id)

    def update_vehicle(self, vehicle_id: int, vehicle: VehicleUpdateDTO) -> VehicleDTO:
        if vehicle_id == 99:
            raise ValueError("Vehicle not found")
        if vehicle.plate == "DUP1A23":
            raise ValueError("Plate already exists")
        return _vehicle(vehicle_id, model=vehicle.model or "Civic")

    def delete_vehicle(self, vehicle_id: int) -> dict:
        if vehicle_id == 99:
            raise ValueError("Vehicle not found")
        return {"ok": True}

    def find_vehicles_by_person_id(self, person_id: str) -> list[VehicleDTO]:
        if person_id == NOT_A_CUSTOMER_CPF:
            raise ValueError("Person not found")
        return [_vehicle()]


def _payload(**overrides) -> VehicleCreateDTO:
    payload = {
        "person_id": VALID_CPF,
        "model": "Civic",
        "brand": "Honda",
        "manufacture_year": "2020",
        "model_year": "2021",
        "engine": "2.0",
        "fuel_type": FuelType.GASOLINE,
        "plate": "ABC1D23",
        "color": "Prata",
    }
    payload.update(overrides)
    return VehicleCreateDTO(**payload)


def test_router_create_accepts_flat_payload():
    result = create_vehicle(_payload(), use_case=_FakeUseCase())
    assert result.vehicle_id == 1
    assert result.model == "Civic"
    assert result.person_id == VALID_CPF
    assert result.plate == "ABC1D23"


def test_router_create_maps_value_error_to_400():
    try:
        create_vehicle(_payload(person_id=NOT_A_CUSTOMER_CPF), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Person is not a customer"
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


def test_router_find_by_person_delegates_to_port():
    result = find_vehicles_by_person_id(VALID_CPF, use_case=_FakeUseCase())
    assert len(result) == 1
    assert result[0].model == "Civic"


def test_router_find_by_person_maps_not_found_to_404():
    try:
        find_vehicles_by_person_id(NOT_A_CUSTOMER_CPF, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Person not found"
    else:
        raise AssertionError("expected HTTPException")
