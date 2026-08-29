from decimal import Decimal

from src.domain.inventory.application.inventory_use_cases import InventoryUseCases
from src.domain.inventory.value_objects.stock_operation_type import StockOperationType
from src.ports.driver.for_manage_inventory.dto.inventory_dto import StockOperationCreateDTO
from src.ports.driver.for_manage_parts.dto.part_dto import PartDTO
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import OrderPartLineDTO
from tests.unit.fakes.in_memory_storage import InMemoryStorage

import pytest


def _storage_with_part(quantity: int = 0, active: bool = True) -> InMemoryStorage:
    storage = InMemoryStorage()
    storage.save_part(
        PartDTO(
            description="Filtro de oleo",
            brand="Bosch",
            manufacturer="Bosch do Brasil",
            unit_price=Decimal("50.00"),
            available_quantity=quantity,
            flag_active=active,
        )
    )
    return storage


def _use_cases(storage: InMemoryStorage | None = None) -> tuple[InventoryUseCases, InMemoryStorage]:
    storage = storage or _storage_with_part()
    return InventoryUseCases(storage=storage), storage


def test_initial_sets_balance_from_zero():
    use_cases, storage = _use_cases()

    result = use_cases.apply_operation(
        StockOperationCreateDTO(
            part_id=1,
            operation_type=StockOperationType.INITIAL,
            quantity=10,
        )
    )

    assert result.available_quantity == 10
    assert result.operation_type is StockOperationType.INITIAL
    assert storage.get_part(1).available_quantity == 10
    assert len(storage.get_stock_operations_by_part_id(1)) == 1


def test_initial_rejects_when_already_stocked():
    use_cases, _ = _use_cases(_storage_with_part(quantity=5))

    with pytest.raises(ValueError, match="Initial stock is already set"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.INITIAL,
                quantity=10,
            )
        )


def test_inbound_adds_quantity():
    use_cases, _ = _use_cases(_storage_with_part(quantity=5))

    result = use_cases.apply_operation(
        StockOperationCreateDTO(
            part_id=1,
            operation_type=StockOperationType.INBOUND,
            quantity=3,
        )
    )

    assert result.available_quantity == 8


def test_inbound_rejects_order_part_id():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="only allowed for OUTBOUND"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.INBOUND,
                quantity=1,
                order_part_id=1,
            )
        )


def test_outbound_requires_order_part_id():
    use_cases, _ = _use_cases(_storage_with_part(quantity=5))

    with pytest.raises(ValueError, match="OUTBOUND requires order_part_id"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.OUTBOUND,
                quantity=1,
            )
        )


def test_outbound_writes_off_order_part_line():
    storage = _storage_with_part(quantity=5)
    storage._save_order_part_line(
        OrderPartLineDTO(order_id=1, part_id=1, quantity=2, total_amount=Decimal("100.00"))
    )
    use_cases, _ = _use_cases(storage)

    result = use_cases.apply_operation(
        StockOperationCreateDTO(
            part_id=1,
            operation_type=StockOperationType.OUTBOUND,
            quantity=2,
            order_part_id=1,
        )
    )

    assert result.available_quantity == 3
    assert result.order_part_id == 1


def test_outbound_rejects_missing_line():
    use_cases, _ = _use_cases(_storage_with_part(quantity=5))

    with pytest.raises(ValueError, match="Order part line not found"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.OUTBOUND,
                quantity=1,
                order_part_id=99,
            )
        )


def test_outbound_rejects_mismatched_part():
    storage = _storage_with_part(quantity=5)
    storage.save_part(
        PartDTO(
            description="Pastilha",
            brand="Bosch",
            manufacturer="Bosch",
            unit_price=Decimal("20.00"),
            available_quantity=5,
        )
    )
    storage._save_order_part_line(
        OrderPartLineDTO(order_id=1, part_id=2, quantity=1, total_amount=Decimal("20.00"))
    )
    use_cases, _ = _use_cases(storage)

    with pytest.raises(ValueError, match="does not match the part"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.OUTBOUND,
                quantity=1,
                order_part_id=1,
            )
        )


def test_outbound_rejects_quantity_above_line():
    storage = _storage_with_part(quantity=10)
    storage._save_order_part_line(
        OrderPartLineDTO(order_id=1, part_id=1, quantity=2, total_amount=Decimal("100.00"))
    )
    use_cases, _ = _use_cases(storage)

    with pytest.raises(ValueError, match="exceeds the order part line"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.OUTBOUND,
                quantity=3,
                order_part_id=1,
            )
        )


def test_outbound_rejects_insufficient_stock():
    storage = _storage_with_part(quantity=1)
    storage._save_order_part_line(
        OrderPartLineDTO(order_id=1, part_id=1, quantity=2, total_amount=Decimal("100.00"))
    )
    use_cases, _ = _use_cases(storage)

    with pytest.raises(ValueError, match="Insufficient stock"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.OUTBOUND,
                quantity=2,
                order_part_id=1,
            )
        )


def test_outbound_rejects_duplicate_write_off():
    storage = _storage_with_part(quantity=5)
    storage._save_order_part_line(
        OrderPartLineDTO(order_id=1, part_id=1, quantity=2, total_amount=Decimal("100.00"))
    )
    use_cases, _ = _use_cases(storage)
    payload = StockOperationCreateDTO(
        part_id=1,
        operation_type=StockOperationType.OUTBOUND,
        quantity=2,
        order_part_id=1,
    )
    use_cases.apply_operation(payload)

    with pytest.raises(ValueError, match="already written off"):
        use_cases.apply_operation(payload)


def test_apply_rejects_unknown_part():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Part not found"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=99,
                operation_type=StockOperationType.INBOUND,
                quantity=1,
            )
        )


def test_apply_rejects_inactive_part():
    use_cases, _ = _use_cases(_storage_with_part(active=False))

    with pytest.raises(ValueError, match="Part is not active"):
        use_cases.apply_operation(
            StockOperationCreateDTO(
                part_id=1,
                operation_type=StockOperationType.INBOUND,
                quantity=1,
            )
        )


def test_read_inventory_returns_balance_and_ledger():
    use_cases, _ = _use_cases()
    use_cases.apply_operation(
        StockOperationCreateDTO(
            part_id=1,
            operation_type=StockOperationType.INITIAL,
            quantity=10,
        )
    )
    use_cases.apply_operation(
        StockOperationCreateDTO(
            part_id=1,
            operation_type=StockOperationType.INBOUND,
            quantity=2,
        )
    )

    detail = use_cases.read_inventory(1)

    assert detail.part_id == 1
    assert detail.available_quantity == 12
    assert [item.operation_type for item in detail.operations] == [
        StockOperationType.INITIAL,
        StockOperationType.INBOUND,
    ]


def test_read_inventory_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Part not found"):
        use_cases.read_inventory(99)


def test_read_quantity_returns_only_balance():
    use_cases, _ = _use_cases()
    use_cases.apply_operation(
        StockOperationCreateDTO(
            part_id=1,
            operation_type=StockOperationType.INITIAL,
            quantity=10,
        )
    )

    quantity = use_cases.read_quantity(1)

    assert quantity.available_quantity == 10
    assert quantity.model_dump() == {"available_quantity": 10}


def test_read_quantity_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Part not found"):
        use_cases.read_quantity(99)
