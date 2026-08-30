from typing import override

from src.domain.inventory.policies.allocate_parts_on_approval import (
    AllocatePartsOnApproval,
)
from src.domain.order_services.entities.order_services import ServiceOrder
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import (
    ForManageInventory,
)
from src.ports.driver.for_manage_quotes.dto.quote_dto import (
    QuoteDecisionDTO,
    QuoteDTO,
    QuoteProductItemDTO,
    QuoteServiceItemDTO,
)
from src.ports.driver.for_manage_quotes.interfaces.for_manage_quote import ForManageQuote
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import ServiceOrderDTO
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData

_QUOTE_READY = frozenset(
    {
        OrderStatus.WAITING_APPROVAL,
        OrderStatus.APPROVED,
        OrderStatus.PARTS_SEPARATING,
        OrderStatus.PARTS_PURCHASING,
        OrderStatus.READY_TO_START,
        OrderStatus.IN_PROGRESS,
        OrderStatus.FINISHED,
        OrderStatus.DELIVERED,
    }
)


class QuoteUseCases(ForManageQuote):
    """HTTP use case: client or shop reads the quote persisted by the policy."""

    def __init__(self, storage: ForStoringData, inventory: ForManageInventory) -> None:
        self._storage = storage
        self._allocate_on_approval = AllocatePartsOnApproval(storage, inventory)

    @override
    def read_quote(self, order_id: int) -> QuoteDTO:
        order = self._storage.get_service_order(order_id)
        if order is None:
            raise ValueError("Order not found")
        if order.status not in _QUOTE_READY:
            raise ValueError("Quote not available")

        vehicle = self._storage.get_vehicle(order.vehicle_id)
        if vehicle is None:
            raise ValueError("Vehicle not found")

        services: list[QuoteServiceItemDTO] = []
        for line in self._storage.get_order_service_lines(order_id):
            service = self._storage.get_service(line.service_id)
            if service is None:
                raise ValueError(f"Service {line.service_id} not found")
            services.append(QuoteServiceItemDTO(description=service.description, price=service.price))

        products: list[QuoteProductItemDTO] = []
        for line in self._storage.get_order_part_lines(order_id):
            part = self._storage.get_part(line.part_id)
            if part is None:
                raise ValueError(f"Part {line.part_id} not found")
            products.append(
                QuoteProductItemDTO(
                    description=part.description,
                    quantity=line.quantity,
                    total_amount=line.total_amount,
                )
            )

        return QuoteDTO(
            vehicle=vehicle,
            services=services,
            products=products,
            total_amount=order.total_amount,
            estimated_duration_days=order.estimated_duration_days,
            notes=order.notes,
        )

    @override
    def decide_quote(self, order_id: int, decision: QuoteDecisionDTO) -> ServiceOrderDTO:
        order = self._storage.get_service_order(order_id)
        if order is None:
            raise ValueError("Order not found")
        if order.status is not OrderStatus.WAITING_APPROVAL:
            raise ValueError("Quote cannot be decided")
        updated = ServiceOrder.model_validate(order).with_status(
            OrderStatus.APPROVED if decision.approved else OrderStatus.REJECTED
        )
        saved = self._storage.save_service_order(ServiceOrderDTO.model_validate(updated))
        if saved.status is OrderStatus.APPROVED:
            saved = self._allocate_on_approval.apply(saved)
        return saved
