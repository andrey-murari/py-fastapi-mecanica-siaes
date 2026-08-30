from decimal import Decimal

from fastapi import HTTPException

from src.domain.relationship.value_objects.fuel_type import FuelType
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_quotes.dto.quote_dto import (
    QuoteDecisionDTO,
    QuoteDTO,
    QuoteProductItemDTO,
    QuoteServiceItemDTO,
)
from src.ports.driver.for_manage_quotes.interfaces.for_manage_quote import ForManageQuote
from src.ports.driver.for_manage_relationship.dto.vehicle_dto import VehicleDTO
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import ServiceOrderDTO
from src.ui.rest.routers.service_orders.quote_router import decide_quote, read_quote


class _FakeUseCase(ForManageQuote):
    def read_quote(self, order_id: int) -> QuoteDTO:
        if order_id == 99:
            raise ValueError("Order not found")
        if order_id == 2:
            raise ValueError("Quote not available")
        return QuoteDTO(
            vehicle=VehicleDTO(
                vehicle_id=1,
                person_id="52998224725",
                model="Civic",
                brand="Honda",
                manufacture_year="2020",
                model_year="2021",
                engine="2.0",
                fuel_type=FuelType.GASOLINE,
                plate="ABC1D23",
                color="Prata",
            ),
            services=[QuoteServiceItemDTO(description="Troca de oleo", price=Decimal("150.00"))],
            products=[
                QuoteProductItemDTO(
                    description="Filtro de oleo",
                    quantity=1,
                    total_amount=Decimal("50.00"),
                )
            ],
            total_amount=Decimal("200.00"),
            estimated_duration_days=1,
        )

    def decide_quote(self, order_id: int, decision: QuoteDecisionDTO) -> ServiceOrderDTO:
        if order_id == 99:
            raise ValueError("Order not found")
        if order_id == 2:
            raise ValueError("Quote cannot be decided")
        return ServiceOrderDTO(
            order_id=order_id,
            person_id="52998224725",
            vehicle_id=1,
            mileage=85000,
            reported_problem="Barulho no motor",
            status=OrderStatus.APPROVED if decision.approved else OrderStatus.REJECTED,
        )


def test_router_read_quote_delegates_to_port():
    result = read_quote(1, use_case=_FakeUseCase())

    assert result.total_amount == Decimal("200.00")
    assert result.estimated_duration_days == 1
    assert result.vehicle.plate == "ABC1D23"


def test_router_read_quote_maps_missing_order_to_404():
    try:
        read_quote(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Order not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_quote_maps_unavailable_to_400():
    try:
        read_quote(2, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Quote not available"
    else:
        raise AssertionError("expected HTTPException")


def test_router_approve_delegates_to_port():
    result = decide_quote(1, QuoteDecisionDTO(approved=True), use_case=_FakeUseCase())

    assert result.status is OrderStatus.APPROVED


def test_router_reject_delegates_to_port():
    result = decide_quote(1, QuoteDecisionDTO(approved=False), use_case=_FakeUseCase())

    assert result.status is OrderStatus.REJECTED


def test_router_decide_maps_missing_order_to_404():
    try:
        decide_quote(99, QuoteDecisionDTO(approved=True), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("expected HTTPException")
