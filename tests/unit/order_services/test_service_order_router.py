from decimal import Decimal

from fastapi import HTTPException

from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderDiagnosisDTO,
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
    submit_diagnosis,
    update_service_order,
)


VALID_CPF = "52998224725"
UNKNOWN_CPF = "11144477735"


def _detail(order_id: int = 1, **overrides) -> ServiceOrderDetailDTO:
    payload = {
        "order_id": order_id,
        "person_id": VALID_CPF,
        "vehicle_id": 1,
        "mileage": 85000,
        "reported_problem": "Barulho no motor ao acelerar",
        "services_total": Decimal("150.00"),
        "total_amount": Decimal("150.00"),
        "services": [OrderServiceLineDTO(order_id=order_id, service_id=1)],
    }
    payload.update(overrides)
    return ServiceOrderDetailDTO(**payload)


class _FakeUseCase(ForManageServiceOrder):
    def create_service_order(self, order: ServiceOrderCreateDTO) -> ServiceOrderDetailDTO:
        if order.person_id == UNKNOWN_CPF:
            raise ValueError("Customer not found")
        return _detail(reported_problem=order.reported_problem)

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
        if mechanic.mechanic_id == "99":
            raise ValueError("Mechanic not found")
        if mechanic.mechanic_id == "2":
            raise ValueError("User is not a mechanic")
        return _detail(
            order_id,
            status=OrderStatus.WAITING_DIAGNOSIS,
            mechanic_id=mechanic.mechanic_id,
            services=[
                OrderServiceLineDTO(order_id=order_id, service_id=1, mechanic_id=mechanic.mechanic_id)
            ],
        )

    def submit_diagnosis(
        self,
        order_id: int,
        diagnosis: OrderDiagnosisDTO,
    ) -> ServiceOrderDetailDTO:
        if order_id == 99:
            raise ValueError("Order not found")
        if order_id == 2:
            raise ValueError("Order is not waiting for diagnosis")
        return _detail(
            order_id,
            diagnosis=diagnosis.diagnosis,
            status=OrderStatus.DIAGNOSIS_COMPLETED,
            services=[
                OrderServiceLineDTO(order_id=order_id, service_id=line.service_id)
                for line in diagnosis.services
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
        "person_id": VALID_CPF,
        "vehicle_id": 1,
        "mileage": 85000,
        "reported_problem": "Barulho no motor ao acelerar",
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
        create_service_order(_payload(person_id=UNKNOWN_CPF), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_create_accepts_order_without_services():
    result = create_service_order(_payload(services=[]), use_case=_FakeUseCase())

    assert result.order_id == 1


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
    result = assign_mechanic(1, AssignMechanicDTO(mechanic_id="1"), use_case=_FakeUseCase())

    assert result.status is OrderStatus.WAITING_DIAGNOSIS
    assert result.services[0].mechanic_id == "1"


def test_router_assign_mechanic_maps_missing_user_to_404():
    try:
        assign_mechanic(1, AssignMechanicDTO(mechanic_id="99"), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Mechanic not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_assign_mechanic_maps_wrong_role_to_400():
    try:
        assign_mechanic(1, AssignMechanicDTO(mechanic_id="2"), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "User is not a mechanic"
    else:
        raise AssertionError("expected HTTPException")


def test_router_submit_diagnosis_delegates_to_port():
    result = submit_diagnosis(
        1,
        OrderDiagnosisDTO(
            diagnosis="Trocar correia",
            services=[OrderServiceCreateDTO(service_id=1)],
        ),
        use_case=_FakeUseCase(),
    )

    assert result.status is OrderStatus.DIAGNOSIS_COMPLETED
    assert result.diagnosis == "Trocar correia"


def test_router_submit_diagnosis_maps_wrong_status_to_400():
    try:
        submit_diagnosis(
            2,
            OrderDiagnosisDTO(
                diagnosis="Trocar correia",
                services=[OrderServiceCreateDTO(service_id=1)],
            ),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Order is not waiting for diagnosis"
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
