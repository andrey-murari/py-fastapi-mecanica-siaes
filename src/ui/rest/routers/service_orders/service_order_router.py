from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderDiagnosisDTO,
    OrderStatusUpdateDTO,
    ServiceOrderCreateDTO,
    ServiceOrderDetailDTO,
    ServiceOrderUpdateDTO,
)
from src.ports.driver.for_manage_service_orders.interfaces.for_manage_service_order import (
    ForManageServiceOrder,
)
from src.ui.rest.dependencies import get_for_manage_service_order, require_admin

service_order_router = APIRouter(
    prefix="/service-order",
    tags=["service-order"],
    dependencies=[Depends(require_admin)],
)

_NOT_FOUND_MESSAGES = frozenset(
    {"Order not found", "Customer not found", "Vehicle not found", "Mechanic not found"}
)


def _raise_http(exc: ValueError) -> HTTPException:
    status_code = 404 if str(exc) in _NOT_FOUND_MESSAGES else 400
    return HTTPException(status_code=status_code, detail=str(exc))


@service_order_router.post("/", response_model=ServiceOrderDetailDTO)
def create_service_order(
    order: ServiceOrderCreateDTO,
    use_case: Annotated[ForManageServiceOrder, Depends(get_for_manage_service_order)],
):
    try:
        return use_case.create_service_order(order)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@service_order_router.get("/{order_id}", response_model=ServiceOrderDetailDTO)
def read_service_order(
    order_id: int,
    use_case: Annotated[ForManageServiceOrder, Depends(get_for_manage_service_order)],
):
    try:
        return use_case.read_service_order(order_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@service_order_router.patch("/{order_id}", response_model=ServiceOrderDetailDTO)
def update_service_order(
    order_id: int,
    order: ServiceOrderUpdateDTO,
    use_case: Annotated[ForManageServiceOrder, Depends(get_for_manage_service_order)],
):
    try:
        return use_case.update_service_order(order_id, order)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@service_order_router.patch("/{order_id}/mechanic", response_model=ServiceOrderDetailDTO)
def assign_mechanic(
    order_id: int,
    mechanic: AssignMechanicDTO,
    use_case: Annotated[ForManageServiceOrder, Depends(get_for_manage_service_order)],
):
    try:
        return use_case.assign_mechanic(order_id, mechanic)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@service_order_router.patch("/{order_id}/diagnosis", response_model=ServiceOrderDetailDTO)
def submit_diagnosis(
    order_id: int,
    diagnosis: OrderDiagnosisDTO,
    use_case: Annotated[ForManageServiceOrder, Depends(get_for_manage_service_order)],
):
    try:
        return use_case.submit_diagnosis(order_id, diagnosis)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@service_order_router.patch("/{order_id}/status", response_model=ServiceOrderDetailDTO)
def change_status(
    order_id: int,
    status: OrderStatusUpdateDTO,
    use_case: Annotated[ForManageServiceOrder, Depends(get_for_manage_service_order)],
):
    try:
        return use_case.change_status(order_id, status)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@service_order_router.delete("/{order_id}")
def delete_service_order(
    order_id: int,
    use_case: Annotated[ForManageServiceOrder, Depends(get_for_manage_service_order)],
):
    try:
        return use_case.delete_service_order(order_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc
