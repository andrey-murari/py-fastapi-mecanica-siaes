from decimal import Decimal

from src.domain.inventory.application.inventory_use_cases import InventoryUseCases
from src.domain.order_services.policies.quote_on_diagnosis_completed import (
    STOCK_SHORTAGE_NOTE,
    QuoteOnDiagnosisCompleted,
    working_days,
)
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.domain.services.application.service_use_cases import ServiceUseCases
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderDiagnosisDTO,
    OrderPartCreateDTO,
    OrderServiceCreateDTO,
)
from tests.unit.order_services.test_service_order_use_cases import MECHANIC_ID, _payload, _seed


def test_policy_requotes_from_live_inventory_and_service_catalog():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload(services=[]))
    use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=MECHANIC_ID))
    use_cases.submit_diagnosis(
        created.order_id,
        OrderDiagnosisDTO(
            diagnosis="Trocar oleo e filtro",
            services=[OrderServiceCreateDTO(service_id=1)],
            parts=[OrderPartCreateDTO(part_id=1, quantity=2)],
        ),
    )

    storage.save_service(
        storage.get_service(1).model_copy(
            update={"price": Decimal("200.00"), "average_duration_minutes": 90}
        )
    )
    storage.save_part(storage.get_part(1).model_copy(update={"unit_price": Decimal("80.00")}))

    quoted = QuoteOnDiagnosisCompleted(
        storage,
        InventoryUseCases(storage),
        ServiceUseCases(storage),
    ).apply(storage.get_service_order(created.order_id))

    stored = storage.get_service_order(created.order_id)
    parts = storage.get_order_part_lines(created.order_id)

    assert quoted.status is OrderStatus.WAITING_APPROVAL
    assert quoted.services_total == Decimal("200.00")
    assert quoted.parts_total == Decimal("160.00")
    assert quoted.total_amount == Decimal("360.00")
    assert quoted.estimated_duration_days == 1
    assert stored.total_amount == Decimal("360.00")
    assert stored.estimated_duration_days == 1
    assert quoted.notes is None
    assert parts[0].total_amount == Decimal("160.00")


def test_policy_adds_days_and_note_when_stock_is_short():
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

    stored = storage.get_service_order(created.order_id)

    assert stored.estimated_duration_days == 8
    assert stored.notes == STOCK_SHORTAGE_NOTE


def test_working_days_uses_eight_hour_workday():
    assert working_days(0) == 0
    assert working_days(1) == 1
    assert working_days(480) == 1
    assert working_days(481) == 2
    assert working_days(960) == 2
    assert working_days(961) == 3
