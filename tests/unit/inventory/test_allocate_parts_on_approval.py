from src.domain.inventory.application.inventory_use_cases import InventoryUseCases
from src.domain.inventory.policies.allocate_parts_on_approval import (
    AllocatePartsOnApproval,
)
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_quotes.dto.quote_dto import QuoteDecisionDTO
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderDiagnosisDTO,
    OrderPartCreateDTO,
    OrderServiceCreateDTO,
)
from src.domain.order_services.application.quote_use_cases import QuoteUseCases
from tests.unit.order_services.test_service_order_use_cases import MECHANIC_ID, _payload, _seed


def test_policy_sends_approved_order_to_separating_when_stock_covers():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload(services=[]))
    use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=MECHANIC_ID))
    use_cases.submit_diagnosis(
        created.order_id,
        OrderDiagnosisDTO(
            diagnosis="Trocar filtro",
            services=[OrderServiceCreateDTO(service_id=1)],
            parts=[OrderPartCreateDTO(part_id=1, quantity=2)],
        ),
    )
    QuoteUseCases(storage=storage, inventory=InventoryUseCases(storage)).decide_quote(
        created.order_id, QuoteDecisionDTO(approved=True)
    )

    stored = storage.get_service_order(created.order_id)
    assert stored.status is OrderStatus.PARTS_SEPARATING


def test_policy_ignores_order_that_is_not_approved():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload())

    result = AllocatePartsOnApproval(storage, InventoryUseCases(storage)).apply(
        storage.get_service_order(created.order_id)
    )

    assert result.status is OrderStatus.WAITING_MECHANIC
