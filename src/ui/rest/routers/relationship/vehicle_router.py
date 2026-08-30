from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.vehicle_dto import (
    VehicleCreateDTO,
    VehicleDTO,
    VehicleUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ui.rest.dependencies import get_for_manage_vehicle, require_admin
from src.ui.rest.http_responses import RESPONSES_400, RESPONSES_400_404, RESPONSES_404

vehicle_router = APIRouter(
    prefix="/vehicle",
    tags=["vehicle"],
    dependencies=[Depends(require_admin)],
)

_NOT_FOUND_MESSAGES = frozenset({"Person not found", "Vehicle not found"})


def _raise_http(exc: ValueError) -> HTTPException:
    status_code = 404 if str(exc) in _NOT_FOUND_MESSAGES else 400
    return HTTPException(status_code=status_code, detail=str(exc))


@vehicle_router.get("/from-person/{person_id}", response_model=list[VehicleDTO], responses=RESPONSES_400_404)
def find_vehicles_by_person_id(
    person_id: str,
    use_case: Annotated[ForManageVehicle, Depends(get_for_manage_vehicle)],
):
    try:
        return use_case.find_vehicles_by_person_id(person_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@vehicle_router.post("/", response_model=VehicleDTO, responses=RESPONSES_400)
def create_vehicle(
    vehicle: VehicleCreateDTO,
    use_case: Annotated[ForManageVehicle, Depends(get_for_manage_vehicle)],
):
    try:
        return use_case.create_vehicle(vehicle)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@vehicle_router.get("/{vehicle_id}", response_model=VehicleDTO, responses=RESPONSES_404)
def read_vehicle(
    vehicle_id: int,
    use_case: Annotated[ForManageVehicle, Depends(get_for_manage_vehicle)],
):
    try:
        return use_case.read_vehicle(vehicle_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@vehicle_router.patch("/{vehicle_id}", response_model=VehicleDTO, responses=RESPONSES_400_404)
def update_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdateDTO,
    use_case: Annotated[ForManageVehicle, Depends(get_for_manage_vehicle)],
):
    try:
        return use_case.update_vehicle(vehicle_id, vehicle)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@vehicle_router.delete("/{vehicle_id}", responses=RESPONSES_404)
def delete_vehicle(
    vehicle_id: int,
    use_case: Annotated[ForManageVehicle, Depends(get_for_manage_vehicle)],
):
    try:
        return use_case.delete_vehicle(vehicle_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
