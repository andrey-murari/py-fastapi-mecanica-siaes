from typing import override

from pydantic import ValidationError

from src.domain.inventory.entities.stock_operation import StockOperation
from src.domain.inventory.value_objects.stock_operation_type import StockOperationType
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_inventory.dto.inventory_dto import (
    InventoryDetailDTO,
    InventoryQuantityDTO,
    StockOperationCreateDTO,
    StockOperationDTO,
    StockOperationResultDTO,
)
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import ForManageInventory
from src.ports.driver.for_manage_parts.dto.part_dto import PartDTO
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class InventoryUseCases(ForManageInventory):
    """Implements the driver port and depends only on driven ports."""

    def __init__(self, storage: ForStoringData) -> None:
        self._storage = storage

    @override
    def apply_operation(self, operation: StockOperationCreateDTO) -> StockOperationResultDTO:
        part = self._require_part(operation.part_id)
        if not part.flag_active:
            raise ValueError("Part is not active")
        try:
            entity = StockOperation(
                part_id=operation.part_id,
                operation_type=operation.operation_type,
                quantity=operation.quantity,
                order_part_id=operation.order_part_id,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc

        new_quantity = self._next_quantity(part, entity)
        updated_part = part.model_copy(update={"available_quantity": new_quantity})
        saved = self._storage.apply_stock_operation(
            StockOperationDTO.model_validate(entity),
            updated_part,
        )
        return StockOperationResultDTO(
            **saved.model_dump(),
            available_quantity=new_quantity,
        )

    @override
    def read_inventory(self, part_id: int) -> InventoryDetailDTO:
        part = self._require_part(part_id)
        operations = sorted(
            self._storage.get_stock_operations_by_part_id(part_id),
            key=lambda item: item.operation_date,
        )
        return InventoryDetailDTO(
            part_id=part_id,
            available_quantity=part.available_quantity,
            operations=operations,
        )

    @override
    def read_quantity(self, part_id: int) -> InventoryQuantityDTO:
        part = self._require_part(part_id)
        return InventoryQuantityDTO(
            available_quantity=part.available_quantity,
            unit_price=part.unit_price,
        )

    def _require_part(self, part_id: int) -> PartDTO:
        part = self._storage.get_part(part_id)
        if part is None:
            raise ValueError("Part not found")
        return part

    def _next_quantity(self, part: PartDTO, operation: StockOperation) -> int:
        if operation.operation_type is StockOperationType.INITIAL:
            if part.available_quantity != 0:
                raise ValueError("Initial stock is already set")
            return operation.quantity
        if operation.operation_type is StockOperationType.INBOUND:
            return part.available_quantity + operation.quantity
        self._assert_outbound(part, operation)
        return part.available_quantity - operation.quantity

    def _assert_outbound(self, part: PartDTO, operation: StockOperation) -> None:
        if operation.order_part_id is None:
            raise ValueError("OUTBOUND requires order_part_id")
        existing = self._storage.get_stock_operation_by_order_part_id(operation.order_part_id)
        if existing is not None:
            raise ValueError("Order part already written off")
        line = self._storage.get_order_part_line(operation.order_part_id)
        if line is None:
            raise ValueError("Order part line not found")
        if line.part_id != part.part_id:
            raise ValueError("Order part line does not match the part")
        if operation.quantity > line.quantity:
            raise ValueError("Quantity exceeds the order part line")
        if operation.quantity > part.available_quantity:
            raise ValueError("Insufficient stock")
