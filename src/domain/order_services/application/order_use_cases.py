from decimal import Decimal
from typing import override

from pydantic import ValidationError

from src.domain.order_services.entities.order_services import (
    OrderPartLine,
    OrderServiceLine,
    ServiceOrder,
)
from src.domain.order_services.value_objects.order_status import OrderStatus
from src.domain.relationship.value_objects.user_type import UserType
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import (
    AssignMechanicDTO,
    OrderPartCreateDTO,
    OrderPartLineDTO,
    OrderServiceCreateDTO,
    OrderServiceLineDTO,
    OrderStatusUpdateDTO,
    ServiceOrderCreateDTO,
    ServiceOrderDetailDTO,
    ServiceOrderDTO,
    ServiceOrderUpdateDTO,
)
from src.ports.driver.for_manage_service_orders.interfaces.for_manage_service_order import (
    ForManageServiceOrder,
)
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class ServiceOrderUseCases(ForManageServiceOrder):
    """Implements the driver port and depends only on driven ports."""

    def __init__(self, storage: ForStoringData) -> None:
        self._storage = storage

    @override
    def create_service_order(self, order: ServiceOrderCreateDTO) -> ServiceOrderDetailDTO:
        customer = self._storage.get_customer(order.customer_id)
        if customer is None:
            raise ValueError("Customer not found")
        if not customer.flag_active:
            raise ValueError("Customer is not active")

        link = self._storage.get_vehicle_customer(order.vehicle_customer_id)
        if link is None:
            raise ValueError("Vehicle not found")
        if link.customer_id != order.customer_id:
            raise ValueError("Vehicle does not belong to the customer")
        if not link.flag_active:
            raise ValueError("Vehicle is not active")

        service_lines, services_total = self._build_service_lines(
            order.services,
            order.user_modification_id,
        )
        part_lines, parts_total = self._build_part_lines(order.parts, order.user_modification_id)

        try:
            entity = ServiceOrder(
                customer_id=order.customer_id,
                vehicle_customer_id=order.vehicle_customer_id,
                mileage=order.mileage,
                user_modification_id=order.user_modification_id,
            ).with_totals(services_total, parts_total)
        except ValidationError as exc:
            raise value_error_from(exc) from exc

        saved = self._storage.save_new_service_order(
            order=ServiceOrderDTO.model_validate(entity),
            service_lines=[OrderServiceLineDTO.model_validate(line) for line in service_lines],
            part_lines=[OrderPartLineDTO.model_validate(line) for line in part_lines],
        )
        return self._detail(saved)

    @override
    def read_service_order(self, order_id: int) -> ServiceOrderDetailDTO:
        return self._detail(self._require_order(order_id))

    @override
    def update_service_order(
        self,
        order_id: int,
        order: ServiceOrderUpdateDTO,
    ) -> ServiceOrderDetailDTO:
        stored = self._require_order(order_id)
        try:
            current = ServiceOrder.model_validate(stored)
            current.ensure_editable()
        except ValidationError as exc:
            raise value_error_from(exc) from exc

        header_changes = order.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={"services", "parts"},
        )
        user_modification_id = order.user_modification_id or stored.user_modification_id

        service_lines = self._storage.get_order_service_lines(order_id)
        part_lines = self._storage.get_order_part_lines(order_id)
        replace_lines = order.services is not None or order.parts is not None

        if order.services is not None:
            new_services, services_total = self._build_service_lines(
                order.services,
                user_modification_id,
                mechanic_id=next(
                    (line.mechanic_id for line in service_lines if line.mechanic_id), None
                ),
            )
            service_lines = [OrderServiceLineDTO.model_validate(line) for line in new_services]
        else:
            services_total = self._services_total(service_lines)

        if order.parts is not None:
            new_parts, parts_total = self._build_part_lines(order.parts, user_modification_id)
            part_lines = [OrderPartLineDTO.model_validate(line) for line in new_parts]
        else:
            parts_total = sum(
                (line.total_amount for line in part_lines),
                start=Decimal("0"),
            )

        try:
            updated = ServiceOrder.model_validate(
                current.model_copy(update=header_changes)
            ).with_totals(services_total, parts_total)
        except ValidationError as exc:
            raise value_error_from(exc) from exc

        saved = self._storage.save_service_order(ServiceOrderDTO.model_validate(updated))
        if replace_lines:
            self._storage.replace_order_lines(
                order_id=order_id,
                service_lines=service_lines,
                part_lines=part_lines,
            )
        return self._detail(saved)

    @override
    def delete_service_order(self, order_id: int) -> dict:
        self._require_order(order_id)
        self._storage.delete_service_order(order_id)
        return {"ok": True}

    @override
    def assign_mechanic(self, order_id: int, mechanic: AssignMechanicDTO) -> ServiceOrderDetailDTO:
        stored = self._require_order(order_id)
        user = self._storage.get_user(mechanic.mechanic_id)
        if user is None:
            raise ValueError("Mechanic not found")
        if not user.flag_active:
            raise ValueError("Mechanic is not active")
        if user.user_type is not UserType.MECHANIC:
            raise ValueError("User is not a mechanic")

        try:
            current = ServiceOrder.model_validate(stored)
            current.ensure_can_receive_mechanic()
            updated = ServiceOrder.model_validate(
                current.with_status(OrderStatus.WAITING_DIAGNOSIS)
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc

        for line in self._storage.get_order_service_lines(order_id):
            try:
                assigned = OrderServiceLine.model_validate(
                    line.model_copy(update={"mechanic_id": mechanic.mechanic_id})
                )
            except ValidationError as exc:
                raise value_error_from(exc) from exc
            self._storage.save_order_service_line(OrderServiceLineDTO.model_validate(assigned))

        saved = self._storage.save_service_order(ServiceOrderDTO.model_validate(updated))
        return self._detail(saved)

    @override
    def change_status(self, order_id: int, status: OrderStatusUpdateDTO) -> ServiceOrderDetailDTO:
        stored = self._require_order(order_id)
        try:
            current = ServiceOrder.model_validate(stored)
            updated = ServiceOrder.model_validate(current.with_status(status.status))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        if status.status is OrderStatus.WAITING_DIAGNOSIS and not any(
            line.mechanic_id for line in self._storage.get_order_service_lines(order_id)
        ):
            raise ValueError("Order has no mechanic assigned")
        saved = self._storage.save_service_order(ServiceOrderDTO.model_validate(updated))
        return self._detail(saved)

    def _require_order(self, order_id: int) -> ServiceOrderDTO:
        order = self._storage.get_service_order(order_id)
        if order is None:
            raise ValueError("Order not found")
        return order

    def _build_service_lines(
        self,
        services: list[OrderServiceCreateDTO],
        user_modification_id: int,
        mechanic_id: int | None = None,
    ) -> tuple[list[OrderServiceLine], Decimal]:
        if not services:
            raise ValueError("Order must contain at least one service")
        lines: list[OrderServiceLine] = []
        total = Decimal("0")
        for requested in services:
            service = self._storage.get_service(requested.service_id)
            if service is None:
                raise ValueError(f"Service {requested.service_id} not found")
            if not service.flag_active:
                raise ValueError(f"Service {requested.service_id} is not active")
            try:
                lines.append(
                    OrderServiceLine(
                        service_id=requested.service_id,
                        mechanic_id=mechanic_id,
                        user_modification_id=user_modification_id,
                    )
                )
            except ValidationError as exc:
                raise value_error_from(exc) from exc
            total += service.price
        return lines, total

    def _build_part_lines(
        self,
        parts: list[OrderPartCreateDTO],
        user_modification_id: int,
    ) -> tuple[list[OrderPartLine], Decimal]:
        lines: list[OrderPartLine] = []
        total = Decimal("0")
        for requested in parts:
            part = self._storage.get_part(requested.part_id)
            if part is None:
                raise ValueError(f"Part {requested.part_id} not found")
            if not part.flag_active:
                raise ValueError(f"Part {requested.part_id} is not active")
            if part.available_quantity < requested.quantity:
                raise ValueError(f"Part {requested.part_id} has insufficient stock")
            line_total = part.unit_price * requested.quantity
            try:
                lines.append(
                    OrderPartLine(
                        part_id=requested.part_id,
                        quantity=requested.quantity,
                        total_amount=line_total,
                        user_modification_id=user_modification_id,
                    )
                )
            except ValidationError as exc:
                raise value_error_from(exc) from exc
            total += line_total
        return lines, total

    def _services_total(self, lines: list[OrderServiceLineDTO]) -> Decimal:
        total = Decimal("0")
        for line in lines:
            service = self._storage.get_service(line.service_id)
            if service is None:
                raise ValueError(f"Service {line.service_id} not found")
            total += service.price
        return total

    def _detail(self, order: ServiceOrderDTO) -> ServiceOrderDetailDTO:
        if order.order_id is None:
            return ServiceOrderDetailDTO(**order.model_dump())
        return ServiceOrderDetailDTO(
            **order.model_dump(),
            services=self._storage.get_order_service_lines(order.order_id),
            parts=self._storage.get_order_part_lines(order.order_id),
        )
