from datetime import datetime
from decimal import Decimal

import pytest

from src.domain.order_services.application.order_use_cases import ServiceOrderUseCases
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.domain.relationship.value_objects.fuel_type import FuelType
from src.domain.relationship.value_objects.user_type import UserType
from src.ports.driver.for_manage_parts.dto.part_dto import PartDTO
from src.ports.driver.for_manage_relationship.dto import (
    CustomerDTO,
    UserDTO,
    VehicleCustomerDTO,
    VehicleDTO,
)
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderPartCreateDTO,
    OrderServiceCreateDTO,
    OrderStatusUpdateDTO,
    ServiceOrderCreateDTO,
    ServiceOrderUpdateDTO,
)
from src.ports.driver.for_manage_services.dto.service_dto import ServiceDTO
from tests.unit.fakes.in_memory_storage import InMemoryStorage

CPF = "52998224725"


def _seed() -> tuple[ServiceOrderUseCases, InMemoryStorage]:
    storage = InMemoryStorage()
    storage.save_customer(CustomerDTO(cpf=CPF, insertion_date=datetime.now()))
    vehicle = storage.save_vehicle(
        VehicleDTO(
            model="Civic",
            brand="Honda",
            manufacture_year="2020",
            model_year="2021",
            engine="2.0",
            fuel_type=FuelType.GASOLINE,
        )
    )
    storage.save_vehicle_customer(
        VehicleCustomerDTO(
            vehicle_id=vehicle.vehicle_id,
            customer_id=1,
            plate="ABC1D23",
            color="Prata",
        )
    )
    storage.save_service(ServiceDTO(description="Troca de oleo", price=Decimal("150.00")))
    storage.save_service(ServiceDTO(description="Alinhamento", price=Decimal("100.00")))
    storage.save_part(
        PartDTO(
            description="Filtro de oleo",
            brand="Bosch",
            manufacturer="Bosch do Brasil",
            unit_price=Decimal("50.00"),
            available_quantity=4,
        )
    )
    storage.save_user(
        UserDTO(user_type=UserType.MECHANIC, login="mecanico", password="secret")
    )
    storage.save_user(UserDTO(user_type=UserType.ADMIN, login="admin", password="secret"))
    return ServiceOrderUseCases(storage=storage), storage


def _payload(**overrides) -> ServiceOrderCreateDTO:
    payload = {
        "customer_id": 1,
        "vehicle_customer_id": 1,
        "mileage": 85000,
        "services": [OrderServiceCreateDTO(service_id=1)],
        "parts": [],
    }
    payload.update(overrides)
    return ServiceOrderCreateDTO(**payload)


def test_create_order_totals_services_and_parts():
    use_cases, _ = _seed()

    order = use_cases.create_service_order(
        _payload(
            services=[OrderServiceCreateDTO(service_id=1), OrderServiceCreateDTO(service_id=2)],
            parts=[OrderPartCreateDTO(part_id=1, quantity=2)],
        )
    )

    assert order.services_total == Decimal("250.00")
    assert order.parts_total == Decimal("100.00")
    assert order.total_amount == Decimal("350.00")
    assert len(order.services) == 2
    assert len(order.parts) == 1


def test_create_order_starts_waiting_for_mechanic():
    use_cases, _ = _seed()

    order = use_cases.create_service_order(_payload())

    assert order.status is OrderStatus.WAITING_MECHANIC
    assert all(line.mechanic_id is None for line in order.services)


def test_create_order_requires_at_least_one_service():
    use_cases, _ = _seed()

    with pytest.raises(ValueError, match="at least one service"):
        use_cases.create_service_order(_payload(services=[]))


def test_create_order_requires_existing_customer():
    use_cases, _ = _seed()

    with pytest.raises(ValueError, match="Customer not found"):
        use_cases.create_service_order(_payload(customer_id=99))


def test_create_order_requires_active_customer():
    use_cases, storage = _seed()
    storage.save_customer(
        storage.get_customer(1).model_copy(update={"flag_active": False})
    )

    with pytest.raises(ValueError, match="Customer is not active"):
        use_cases.create_service_order(_payload())


def test_create_order_requires_vehicle_of_the_customer():
    use_cases, storage = _seed()
    storage.save_customer(CustomerDTO(cpf="11144477735", insertion_date=datetime.now()))

    with pytest.raises(ValueError, match="Vehicle does not belong to the customer"):
        use_cases.create_service_order(_payload(customer_id=2))


def test_create_order_rejects_unknown_service():
    use_cases, _ = _seed()

    with pytest.raises(ValueError, match="Service 9 not found"):
        use_cases.create_service_order(_payload(services=[OrderServiceCreateDTO(service_id=9)]))


def test_create_order_rejects_inactive_service():
    use_cases, storage = _seed()
    storage.save_service(storage.get_service(1).model_copy(update={"flag_active": False}))

    with pytest.raises(ValueError, match="Service 1 is not active"):
        use_cases.create_service_order(_payload())


def test_create_order_rejects_insufficient_stock():
    use_cases, _ = _seed()

    with pytest.raises(ValueError, match="insufficient stock"):
        use_cases.create_service_order(
            _payload(parts=[OrderPartCreateDTO(part_id=1, quantity=10)])
        )


def test_read_order_returns_lines():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(
        _payload(parts=[OrderPartCreateDTO(part_id=1, quantity=1)])
    )

    order = use_cases.read_service_order(created.order_id)

    assert order.order_id == created.order_id
    assert len(order.services) == 1
    assert len(order.parts) == 1


def test_read_order_not_found():
    use_cases, _ = _seed()

    with pytest.raises(ValueError, match="Order not found"):
        use_cases.read_service_order(99)


def test_update_order_replaces_services_and_recalculates_totals():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())

    updated = use_cases.update_service_order(
        created.order_id,
        ServiceOrderUpdateDTO(services=[OrderServiceCreateDTO(service_id=2)], mileage=90000),
    )

    assert updated.mileage == 90000
    assert updated.services_total == Decimal("100.00")
    assert [line.service_id for line in updated.services] == [2]


def test_update_order_keeps_assigned_mechanic_on_new_lines():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())
    use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=1))

    updated = use_cases.update_service_order(
        created.order_id,
        ServiceOrderUpdateDTO(services=[OrderServiceCreateDTO(service_id=2)]),
    )

    assert [line.mechanic_id for line in updated.services] == [1]


def test_update_order_rejects_finished_order():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload())
    storage.save_service_order(
        storage.get_service_order(created.order_id).model_copy(
            update={"status": OrderStatus.DELIVERED}
        )
    )

    with pytest.raises(ValueError, match="cannot be changed"):
        use_cases.update_service_order(created.order_id, ServiceOrderUpdateDTO(mileage=1))


def test_delete_order_removes_header_and_lines():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(
        _payload(parts=[OrderPartCreateDTO(part_id=1, quantity=1)])
    )

    assert use_cases.delete_service_order(created.order_id) == {"ok": True}
    assert storage.get_service_order(created.order_id) is None
    assert storage.get_order_service_lines(created.order_id) == []
    assert storage.get_order_part_lines(created.order_id) == []


def test_assign_mechanic_moves_order_to_waiting_diagnosis():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())

    order = use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=1))

    assert order.status is OrderStatus.WAITING_DIAGNOSIS
    assert [line.mechanic_id for line in order.services] == [1]


def test_assign_mechanic_requires_mechanic_role():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())

    with pytest.raises(ValueError, match="User is not a mechanic"):
        use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=2))


def test_assign_mechanic_requires_existing_user():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())

    with pytest.raises(ValueError, match="Mechanic not found"):
        use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=99))


def test_assign_mechanic_requires_active_user():
    use_cases, storage = _seed()
    created = use_cases.create_service_order(_payload())
    storage.save_user(storage.get_user(1).model_copy(update={"flag_active": False}))

    with pytest.raises(ValueError, match="Mechanic is not active"):
        use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=1))


def test_assign_mechanic_rejects_order_already_diagnosed():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())
    use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=1))

    with pytest.raises(ValueError, match="not waiting for a mechanic"):
        use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=1))


def test_change_status_follows_the_state_machine():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())
    use_cases.assign_mechanic(created.order_id, AssignMechanicDTO(mechanic_id=1))

    approval = use_cases.change_status(
        created.order_id, OrderStatusUpdateDTO(status=OrderStatus.WAITING_APPROVAL)
    )
    in_progress = use_cases.change_status(
        created.order_id, OrderStatusUpdateDTO(status=OrderStatus.IN_PROGRESS)
    )
    finished = use_cases.change_status(
        created.order_id, OrderStatusUpdateDTO(status=OrderStatus.FINISHED)
    )

    assert approval.status is OrderStatus.WAITING_APPROVAL
    assert in_progress.start_date is not None
    assert finished.end_date is not None


def test_change_status_rejects_invalid_transition():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())

    with pytest.raises(ValueError, match="Cannot change status"):
        use_cases.change_status(
            created.order_id, OrderStatusUpdateDTO(status=OrderStatus.FINISHED)
        )


def test_change_status_to_waiting_diagnosis_requires_mechanic():
    use_cases, _ = _seed()
    created = use_cases.create_service_order(_payload())

    with pytest.raises(ValueError, match="no mechanic assigned"):
        use_cases.change_status(
            created.order_id, OrderStatusUpdateDTO(status=OrderStatus.WAITING_DIAGNOSIS)
        )
