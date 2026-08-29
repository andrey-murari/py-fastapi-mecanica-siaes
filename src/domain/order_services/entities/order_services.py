from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.domain.order_services.value_objects.order_status import (
    ALLOWED_TRANSITIONS,
    OrderStatus,
)


class OrderServiceLine(BaseModel):
    """A service performed under an order, optionally bound to a mechanic."""

    model_config = ConfigDict(from_attributes=True)

    order_service_id: int | None = None
    order_id: int | None = None
    service_id: int = Field(gt=0)
    mechanic_id: int | None = Field(default=None, gt=0)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class OrderPartLine(BaseModel):
    """A part consumed by an order, priced when the order was placed."""

    model_config = ConfigDict(from_attributes=True)

    order_part_id: int | None = None
    order_id: int | None = None
    part_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    total_amount: Decimal = Field(ge=0)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class ServiceOrder(BaseModel):
    """Order header: who asked, for which vehicle, and how much it costs."""

    model_config = ConfigDict(from_attributes=True)

    order_id: int | None = None
    customer_id: int = Field(gt=0)
    vehicle_customer_id: int = Field(gt=0)
    mileage: int = Field(ge=0)
    services_total: Decimal = Field(default=Decimal("0"), ge=0)
    parts_total: Decimal = Field(default=Decimal("0"), ge=0)
    total_amount: Decimal = Field(default=Decimal("0"), ge=0)
    status: OrderStatus = Field(default=OrderStatus.WAITING_MECHANIC)
    request_date: datetime = Field(default_factory=datetime.now)
    start_date: datetime | None = None
    end_date: datetime | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @model_validator(mode="after")
    def validate_totals_and_dates(self) -> "ServiceOrder":
        if self.total_amount != self.services_total + self.parts_total:
            raise ValueError("Total amount must be the sum of services and parts")
        if self.end_date is not None and self.start_date is None:
            raise ValueError("Order cannot be finished before it starts")
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError("End date cannot be before start date")
        return self

    def with_totals(self, services_total: Decimal, parts_total: Decimal) -> "ServiceOrder":
        return self.model_copy(
            update={
                "services_total": services_total,
                "parts_total": parts_total,
                "total_amount": services_total + parts_total,
            }
        )

    def with_status(self, status: OrderStatus) -> "ServiceOrder":
        if status not in ALLOWED_TRANSITIONS[self.status]:
            raise ValueError(f"Cannot change status from {self.status} to {status}")
        update: dict = {"status": status, "modification_date": datetime.now()}
        if status is OrderStatus.IN_PROGRESS and self.start_date is None:
            update["start_date"] = datetime.now()
        if status is OrderStatus.FINISHED and self.end_date is None:
            update["start_date"] = self.start_date or datetime.now()
            update["end_date"] = datetime.now()
        return self.model_copy(update=update)

    def ensure_can_receive_mechanic(self) -> None:
        if self.status is not OrderStatus.WAITING_MECHANIC:
            raise ValueError("Order is not waiting for a mechanic")

    def ensure_editable(self) -> None:
        if self.status in (OrderStatus.FINISHED, OrderStatus.DELIVERED, OrderStatus.CANCELLED):
            raise ValueError(f"Order in status {self.status} cannot be changed")
