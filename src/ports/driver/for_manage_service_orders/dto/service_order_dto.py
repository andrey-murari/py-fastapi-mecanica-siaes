from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.domain.order_services.value_objects.order_status import OrderStatus


class OrderServiceLineDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_service_id: int | None = None
    order_id: int | None = None
    service_id: int
    mechanic_id: int | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class OrderPartLineDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_part_id: int | None = None
    order_id: int | None = None
    part_id: int
    quantity: int
    total_amount: Decimal
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class ServiceOrderDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int | None = None
    customer_id: int
    vehicle_customer_id: int
    mileage: int
    services_total: Decimal = Field(default=Decimal("0"))
    parts_total: Decimal = Field(default=Decimal("0"))
    total_amount: Decimal = Field(default=Decimal("0"))
    status: OrderStatus = Field(default=OrderStatus.WAITING_MECHANIC)
    request_date: datetime = Field(default_factory=datetime.now)
    start_date: datetime | None = None
    end_date: datetime | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class OrderServiceCreateDTO(BaseModel):
    service_id: int = Field(examples=[1])


class OrderPartCreateDTO(BaseModel):
    part_id: int = Field(examples=[1])
    quantity: int = Field(examples=[2])


class ServiceOrderCreateDTO(BaseModel):
    customer_id: int = Field(examples=[1])
    vehicle_customer_id: int = Field(examples=[1])
    mileage: int = Field(examples=[85000])
    services: list[OrderServiceCreateDTO]
    parts: list[OrderPartCreateDTO] = Field(default_factory=list)
    user_modification_id: int = Field(default=1)


class ServiceOrderUpdateDTO(BaseModel):
    mileage: int | None = None
    services: list[OrderServiceCreateDTO] | None = None
    parts: list[OrderPartCreateDTO] | None = None
    user_modification_id: int | None = None
    flag_active: bool | None = None


class AssignMechanicDTO(BaseModel):
    mechanic_id: int = Field(examples=[1])


class OrderStatusUpdateDTO(BaseModel):
    status: OrderStatus


class ServiceOrderDetailDTO(ServiceOrderDTO):
    services: list[OrderServiceLineDTO] = Field(default_factory=list)
    parts: list[OrderPartLineDTO] = Field(default_factory=list)
