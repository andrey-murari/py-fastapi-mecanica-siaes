from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.domain.order_services.value_objects.order_status import OrderStatus


class OrderServiceLineDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_service_id: int | None = None
    order_id: int | None = None
    service_id: int
    mechanic_id: str | None = None
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
    person_id: str
    vehicle_id: int
    mileage: int
    reported_problem: str
    diagnosis: str | None = None
    mechanic_id: str | None = None
    services_total: Decimal = Field(default=Decimal("0"))
    parts_total: Decimal = Field(default=Decimal("0"))
    total_amount: Decimal = Field(default=Decimal("0"))
    estimated_duration_days: int = Field(default=0, ge=0)
    notes: str | None = None
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
    person_id: str = Field(examples=["52998224725"])
    vehicle_id: int = Field(examples=[1])
    mileage: int = Field(examples=[85000])
    reported_problem: str = Field(
        min_length=1,
        max_length=2000,
        examples=["Barulho no motor ao acelerar"],
    )
    services: list[OrderServiceCreateDTO] = Field(default_factory=list)
    parts: list[OrderPartCreateDTO] = Field(default_factory=list)
    user_modification_id: int = Field(default=1)


class OrderDiagnosisDTO(BaseModel):
    diagnosis: str = Field(
        min_length=1,
        max_length=2000,
        examples=["Correia dentada gasta. Trocar correia e tensor."],
    )
    services: list[OrderServiceCreateDTO] = Field(min_length=1)
    parts: list[OrderPartCreateDTO] = Field(default_factory=list)
    user_modification_id: int = Field(default=1)


class ServiceOrderUpdateDTO(BaseModel):
    mileage: int | None = None
    services: list[OrderServiceCreateDTO] | None = None
    parts: list[OrderPartCreateDTO] | None = None
    user_modification_id: int | None = None
    flag_active: bool | None = None


class AssignMechanicDTO(BaseModel):
    mechanic_id: str = Field(examples=["39053344705"])


class OrderStatusUpdateDTO(BaseModel):
    status: OrderStatus


class ServiceOrderDetailDTO(ServiceOrderDTO):
    services: list[OrderServiceLineDTO] = Field(default_factory=list)
    parts: list[OrderPartLineDTO] = Field(default_factory=list)
