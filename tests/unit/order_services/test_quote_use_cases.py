from decimal import Decimal

import pytest

from src.domain.inventory.application.inventory_use_cases import InventoryUseCases
from src.domain.order_services.application.quote_use_cases import QuoteUseCases
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_quotes.dto.quote_dto import QuoteDecisionDTO
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderDiagnosisDTO,
    OrderPartCreateDTO,
    OrderServiceCreateDTO,
)
from tests.unit.order_services.test_service_order_use_cases import MECHANIC_ID, _payload, _seed


def _quote_ready():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload(services=[]))
    use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=MECHANIC_ID))
    use_cases.submit_diagnosis(
        created.order_id,
        OrderDiagnosisDTO(
            diagnosis="Trocar oleo e filtro",
            services=[OrderServiceCreateDTO(service_id=1), OrderServiceCreateDTO(service_id=2)],
            parts=[OrderPartCreateDTO(part_id=1, quantity=2)],
        ),
    )
    return QuoteUseCases(storage=storage, inventory=InventoryUseCases(storage)), created.order_id


def test_read_quote_returns_vehicle_services_products_total_and_days():
    quotes, order_id = _quote_ready()

    quote = quotes.read_quote(order_id)

    assert quote.vehicle.plate == "ABC1D23"
    assert quote.vehicle.model == "Civic"
    assert [item.description for item in quote.services] == ["Troca de oleo", "Alinhamento"]
    assert [item.price for item in quote.services] == [Decimal("150.00"), Decimal("100.00")]
    assert len(quote.products) == 1
    assert quote.products[0].description == "Filtro de oleo"
    assert quote.products[0].quantity == 2
    assert quote.products[0].total_amount == Decimal("100.00")
    assert quote.total_amount == Decimal("350.00")
    assert quote.estimated_duration_days == 1
    assert quote.notes is None


def test_read_quote_requires_diagnosis():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload())
    quotes = QuoteUseCases(storage=storage, inventory=InventoryUseCases(storage))

    with pytest.raises(ValueError, match="Quote not available"):
        quotes.read_quote(created.order_id)


def test_read_quote_not_found():
    _, storage = _seed()

    with pytest.raises(ValueError, match="Order not found"):
        QuoteUseCases(storage=storage, inventory=InventoryUseCases(storage)).read_quote(99)


def test_approve_quote_separates_parts_when_stock_covers_the_order():
    quotes, order_id = _quote_ready()

    order = quotes.decide_quote(order_id, QuoteDecisionDTO(approved=True))

    assert order.status is OrderStatus.PARTS_SEPARATING


def test_approve_quote_starts_purchase_when_stock_is_short():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload(services=[]))
    use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=MECHANIC_ID))
    use_cases.submit_diagnosis(
        created.order_id,
        OrderDiagnosisDTO(
            diagnosis="Trocar filtro",
            services=[OrderServiceCreateDTO(service_id=1)],
            parts=[OrderPartCreateDTO(part_id=1, quantity=10)],
        ),
    )

    order = QuoteUseCases(storage=storage, inventory=InventoryUseCases(storage)).decide_quote(
        created.order_id, QuoteDecisionDTO(approved=True)
    )

    assert order.status is OrderStatus.PARTS_PURCHASING


def test_reject_quote_marks_order_rejected():
    quotes, order_id = _quote_ready()

    order = quotes.decide_quote(order_id, QuoteDecisionDTO(approved=False))

    assert order.status is OrderStatus.REJECTED


def test_decide_quote_requires_waiting_approval():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload())
    quotes = QuoteUseCases(storage=storage, inventory=InventoryUseCases(storage))

    with pytest.raises(ValueError, match="Quote cannot be decided"):
        quotes.decide_quote(created.order_id, QuoteDecisionDTO(approved=True))
