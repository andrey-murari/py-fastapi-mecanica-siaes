from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_inventory.dto.inventory_dto import (
    InventoryDetailDTO,
    InventoryQuantityDTO,
    StockOperationCreateDTO,
    StockOperationResultDTO,
)
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import (
    ForManageInventory,
)
from src.ui.rest.dependencies import get_for_manage_inventory, require_admin

inventory_router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(require_admin)],
)

_NOT_FOUND_MESSAGES = frozenset({"Part not found", "Order part line not found"})


def _raise_http(exc: ValueError) -> HTTPException:
    status_code = 404 if str(exc) in _NOT_FOUND_MESSAGES else 400
    return HTTPException(status_code=status_code, detail=str(exc))


@inventory_router.post("/", response_model=StockOperationResultDTO)
def apply_operation(
    operation: StockOperationCreateDTO,
    use_case: ForManageInventory = Depends(get_for_manage_inventory),
):
    try:
        return use_case.apply_operation(operation)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@inventory_router.get("/{part_id}/quantity", response_model=InventoryQuantityDTO)
def read_quantity(
    part_id: int,
    use_case: ForManageInventory = Depends(get_for_manage_inventory),
):
    try:
        return use_case.read_quantity(part_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@inventory_router.get("/{part_id}", response_model=InventoryDetailDTO)
def read_inventory(
    part_id: int,
    use_case: ForManageInventory = Depends(get_for_manage_inventory),
):
    try:
        return use_case.read_inventory(part_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc
