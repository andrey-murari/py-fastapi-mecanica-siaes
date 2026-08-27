from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.vehicle_dto import (
    VehicleCreateDTO,
    VehicleDetailDTO,
    VehicleDTO,
    VehicleUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ui.rest.dependencies import get_for_manage_vehicle, require_admin

vehicle_router = APIRouter(
    prefix="/vehicle",
    tags=["vehicle"],
    dependencies=[Depends(require_admin)],
)


@vehicle_router.get("/from-cpf/{cpf}", response_model=list[VehicleDetailDTO])
def find_vehicles_by_customer_cpf(
    cpf: str,
    use_case: ForManageVehicle = Depends(get_for_manage_vehicle),
):
    try:
        return use_case.find_vehicles_by_customer_cpf(cpf)
    except ValueError as exc:
        status_code = 404 if str(exc) == "Customer not found" else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@vehicle_router.post("/", response_model=VehicleDTO)
def create_vehicle(
    vehicle: VehicleCreateDTO,
    use_case: ForManageVehicle = Depends(get_for_manage_vehicle),
):
    try:
        return use_case.create_vehicle(vehicle)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@vehicle_router.get("/{vehicle_id}", response_model=VehicleDetailDTO)
def read_vehicle(
    vehicle_id: int,
    use_case: ForManageVehicle = Depends(get_for_manage_vehicle),
):
    try:
        return use_case.read_vehicle(vehicle_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@vehicle_router.patch("/{vehicle_id}", response_model=VehicleDTO)
def update_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdateDTO,
    use_case: ForManageVehicle = Depends(get_for_manage_vehicle),
):
    try:
        return use_case.update_vehicle(vehicle_id, vehicle)
    except ValueError as exc:
        status_code = 404 if str(exc) == "Vehicle not found" else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@vehicle_router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    use_case: ForManageVehicle = Depends(get_for_manage_vehicle),
):
    try:
        return use_case.delete_vehicle(vehicle_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
