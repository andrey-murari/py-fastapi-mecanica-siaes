from decimal import Decimal
from math import ceil

from src.domain.order_services.entities.order_services import ServiceOrder
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import ForManageInventory
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    OrderPartLineDTO,
    ServiceOrderDTO,
)
from src.ports.driver.for_manage_services.interfaces.for_manage_service import ForManageService
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData

MINUTES_PER_WORKDAY = 8 * 60
STOCK_SHORTAGE_DAYS = 7
STOCK_SHORTAGE_NOTE = (
    "Sera necessaria a compra de algumas pecas para o cliente."
)


def working_days(minutes: int) -> int:
    """8h workday. Anything under a day rounds up to 1; 8h+1min → 2; 16h+1min → 3."""
    return 0 if minutes <= 0 else ceil(minutes / MINUTES_PER_WORKDAY)


class QuoteOnDiagnosisCompleted:
    """DDD policy: runs by itself after Diagnóstico concluído. Not an HTTP use case.

    Recalculates the order budget and time estimate from current inventory and
    service catalog prices.
    """

    def __init__(
        self,
        storage: ForStoringData,
        inventory: ForManageInventory,
        services: ForManageService,
    ) -> None:
        self._storage = storage
        self._inventory = inventory
        self._services = services

    def apply(self, order: ServiceOrderDTO) -> ServiceOrderDTO:
        if order.order_id is None:
            return order

        service_lines = self._storage.get_order_service_lines(order.order_id)
        part_lines = self._storage.get_order_part_lines(order.order_id)

        services_total = Decimal("0")
        estimated_duration_minutes = 0
        for line in service_lines:
            service = self._services.read_service(line.service_id)
            services_total += service.price
            estimated_duration_minutes += service.average_duration_minutes

        quoted_parts: list[OrderPartLineDTO] = []
        parts_total = Decimal("0")
        needs_purchase = False
        for line in part_lines:
            stock = self._inventory.read_quantity(line.part_id)
            if stock.available_quantity < line.quantity:
                needs_purchase = True
            line_total = stock.unit_price * line.quantity
            quoted_parts.append(line.model_copy(update={"total_amount": line_total}))
            parts_total += line_total

        days = working_days(estimated_duration_minutes)
        notes = None
        if needs_purchase:
            days += STOCK_SHORTAGE_DAYS
            notes = STOCK_SHORTAGE_NOTE
        quoted = ServiceOrder.model_validate(order).with_totals(
            services_total, parts_total
        ).model_copy(update={"estimated_duration_days": days, "notes": notes})
        if quoted.status is OrderStatus.DIAGNOSIS_COMPLETED:
            quoted = quoted.with_status(OrderStatus.WAITING_APPROVAL)
        saved = self._storage.save_service_order(ServiceOrderDTO.model_validate(quoted))
        self._storage.replace_order_lines(
            order_id=order.order_id,
            service_lines=service_lines,
            part_lines=quoted_parts,
        )
        return saved
