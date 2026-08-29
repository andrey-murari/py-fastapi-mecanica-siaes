from fastapi import HTTPException

from src.domain.inventory.value_objects.stock_operation_type import StockOperationType
from src.ports.driver.for_manage_inventory.dto.inventory_dto import (
    InventoryDetailDTO,
    InventoryQuantityDTO,
    StockOperationCreateDTO,
    StockOperationDTO,
    StockOperationResultDTO,
)
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import (
    ForManageInventory,
)
from src.ui.rest.routers.inventory.inventory_router import (
    apply_operation,
    read_inventory,
    read_quantity,
)


class _FakeUseCase(ForManageInventory):
    def apply_operation(self, operation: StockOperationCreateDTO) -> StockOperationResultDTO:
        if operation.part_id == 99:
            raise ValueError("Part not found")
        if operation.order_part_id == 99:
            raise ValueError("Order part line not found")
        if operation.operation_type is StockOperationType.INITIAL and operation.quantity == 1:
            raise ValueError("Initial stock is already set")
        return StockOperationResultDTO(
            operation_id=1,
            part_id=operation.part_id,
            operation_type=operation.operation_type,
            quantity=operation.quantity,
            order_part_id=operation.order_part_id,
            available_quantity=operation.quantity,
        )

    def read_inventory(self, part_id: int) -> InventoryDetailDTO:
        if part_id == 99:
            raise ValueError("Part not found")
        return InventoryDetailDTO(
            part_id=part_id,
            available_quantity=10,
            operations=[
                StockOperationDTO(
                    operation_id=1,
                    part_id=part_id,
                    operation_type=StockOperationType.INITIAL,
                    quantity=10,
                )
            ],
        )

    def read_quantity(self, part_id: int) -> InventoryQuantityDTO:
        if part_id == 99:
            raise ValueError("Part not found")
        return InventoryQuantityDTO(available_quantity=10)


def test_router_apply_delegates_to_port():
    result = apply_operation(
        StockOperationCreateDTO(
            part_id=1,
            operation_type=StockOperationType.INITIAL,
            quantity=10,
        ),
        use_case=_FakeUseCase(),
    )

    assert result.operation_id == 1
    assert result.available_quantity == 10


def test_router_apply_maps_missing_part_to_404():
    try:
        apply_operation(
            StockOperationCreateDTO(
                part_id=99,
                operation_type=StockOperationType.INBOUND,
                quantity=1,
            ),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Part not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_apply_maps_missing_line_to_404():
    try:
        apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.OUTBOUND,
                quantity=1,
                order_part_id=99,
            ),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Order part line not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_apply_maps_rule_violation_to_400():
    try:
        apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.INITIAL,
                quantity=1,
            ),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Initial stock is already set"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_delegates_to_port():
    result = read_inventory(1, use_case=_FakeUseCase())

    assert result.available_quantity == 10
    assert len(result.operations) == 1


def test_router_read_maps_missing_part_to_404():
    try:
        read_inventory(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Part not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_quantity_delegates_to_port():
    result = read_quantity(1, use_case=_FakeUseCase())

    assert result.available_quantity == 10
    assert result.model_dump() == {"available_quantity": 10}


def test_router_read_quantity_maps_missing_part_to_404():
    try:
        read_quantity(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Part not found"
    else:
        raise AssertionError("expected HTTPException")
