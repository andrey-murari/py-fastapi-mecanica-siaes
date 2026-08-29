from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_services.dto.service_dto import (
    ServiceCreateDTO,
    ServiceDTO,
    ServiceUpdateDTO,
)
from src.ports.driver.for_manage_services.interfaces.for_manage_service import ForManageService
from src.ui.rest.dependencies import get_for_manage_service, require_admin

service_router = APIRouter(
    prefix="/service",
    tags=["service"],
    dependencies=[Depends(require_admin)],
)


@service_router.post("/", response_model=ServiceDTO)
def create_service(
    service: ServiceCreateDTO,
    use_case: ForManageService = Depends(get_for_manage_service),
):
    try:
        return use_case.create_service(service)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@service_router.get("/{service_id}", response_model=ServiceDTO)
def read_service(
    service_id: int,
    use_case: ForManageService = Depends(get_for_manage_service),
):
    try:
        return use_case.read_service(service_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@service_router.patch("/{service_id}", response_model=ServiceDTO)
def update_service(
    service_id: int,
    service: ServiceUpdateDTO,
    use_case: ForManageService = Depends(get_for_manage_service),
):
    try:
        return use_case.update_service(service_id, service)
    except ValueError as exc:
        status_code = 404 if str(exc) == "Service not found" else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@service_router.delete("/{service_id}")
def delete_service(
    service_id: int,
    use_case: ForManageService = Depends(get_for_manage_service),
):
    try:
        return use_case.delete_service(service_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
