from decimal import Decimal

from fastapi import HTTPException

from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderServiceCreateDTO,
    OrderServiceLineDTO,
    OrderStatusUpdateDTO,
    ServiceOrderCreateDTO,
    ServiceOrderDetailDTO,
    ServiceOrderUpdateDTO,
)
from src.ports.driver.for_manage_service_orders.interfaces.for_manage_service_order import (
    ForManageServiceOrder,
)
from src.ui.rest.routers.service_orders.service_order_router import (
    assign_mechanic,
    change_status,
    create_service_order,
    delete_service_order,
    read_service_order,
    update_service_order,
)


def _detail(order_id: int = 1, **overrides) -> ServiceOrderDetailDTO:
    payload = {
        "order_id": order_id,
        "customer_id": 1,
        "vehicle_customer_id": 1,
        "mileage": 85000,
        "services_total": Decimal("150.00"),
        "total_amount": Decimal("150.00"),
        "services": [OrderServiceLineDTO(order_id=order_id, service_id=1)],
    }
    payload.update(overrides)
    return ServiceOrderDetailDTO(**payload)


class _FakeUseCase(ForManageServiceOrder):
    def create_service_order(self, order: ServiceOrderCreateDTO) -> ServiceOrderDetailDTO:
        if order.customer_id == 99:
            raise ValueError("Customer not found")
        if not order.services:
            raise ValueError("Order must contain at least one service")
        return _detail()

    def read_service_order(self, order_id: int) -> ServiceOrderDetailDTO:
        if order_id == 99:
            raise ValueError("Order not found")
        return _detail(order_id)

    def update_service_order(
        self,
        order_id: int,
        order: ServiceOrderUpdateDTO,
    ) -> ServiceOrderDetailDTO:
        if order_id == 99:
            raise ValueError("Order not found")
        return _detail(order_id, mileage=order.mileage or 85000)

    def delete_service_order(self, order_id: int) -> dict:
        if order_id == 99:
            raise ValueError("Order not found")
        return {"ok": True}

    def assign_mechanic(
        self,
        order_id: int,
        mechanic: AssignMechanicDTO,
    ) -> ServiceOrderDetailDTO:
        if mechanic.mechanic_id == 99:
            raise ValueError("Mechanic not found")
        if mechanic.mechanic_id == 2:
            raise ValueError("User is not a mechanic")
        return _detail(
            order_id,
            status=OrderStatus.WAITING_DIAGNOSIS,
            services=[
                OrderServiceLineDTO(order_id=order_id, service_id=1, mechanic_id=mechanic.mechanic_id)
            ],
        )

    def change_status(
        self,
        order_id: int,
        status: OrderStatusUpdateDTO,
    ) -> ServiceOrderDetailDTO:
        if status.status is OrderStatus.FINISHED:
            raise ValueError("Cannot change status from Aguardando mecânico to Finalizada")
        return _detail(order_id, status=status.status)


def _payload(**overrides) -> ServiceOrderCreateDTO:
    payload = {
        "customer_id": 1,
        "vehicle_customer_id": 1,
        "mileage": 85000,
        "services": [OrderServiceCreateDTO(service_id=1)],
    }
    payload.update(overrides)
    return ServiceOrderCreateDTO(**payload)


def test_router_create_delegates_to_port():
    result = create_service_order(_payload(), use_case=_FakeUseCase())

    assert result.order_id == 1
    assert result.total_amount == Decimal("150.00")


def test_router_create_maps_missing_customer_to_404():
    try:
        create_service_order(_payload(customer_id=99), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_create_maps_rule_violation_to_400():
    try:
        create_service_order(_payload(services=[]), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Order must contain at least one service"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_missing_order_to_404():
    try:
        read_service_order(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Order not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_delegates_to_port():
    result = update_service_order(
        1, ServiceOrderUpdateDTO(mileage=90000), use_case=_FakeUseCase()
    )

    assert result.mileage == 90000


def test_router_assign_mechanic_delegates_to_port():
    result = assign_mechanic(1, AssignMechanicDTO(mechanic_id=1), use_case=_FakeUseCase())

    assert result.status is OrderStatus.WAITING_DIAGNOSIS
    assert result.services[0].mechanic_id == 1


def test_router_assign_mechanic_maps_missing_user_to_404():
    try:
        assign_mechanic(1, AssignMechanicDTO(mechanic_id=99), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Mechanic not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_assign_mechanic_maps_wrong_role_to_400():
    try:
        assign_mechanic(1, AssignMechanicDTO(mechanic_id=2), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "User is not a mechanic"
    else:
        raise AssertionError("expected HTTPException")


def test_router_change_status_maps_invalid_transition_to_400():
    try:
        change_status(
            1, OrderStatusUpdateDTO(status=OrderStatus.FINISHED), use_case=_FakeUseCase()
        )
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("expected HTTPException")


def test_router_delete_maps_missing_order_to_404():
    try:
        delete_service_order(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("expected HTTPException")
