from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ServiceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    service_id: int | None = None
    description: str
    price: Decimal
    average_duration_minutes: int = Field(default=60, ge=0)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class ServiceCreateDTO(BaseModel):
    description: str = Field(examples=["Troca de oleo"])
    price: Decimal = Field(examples=["150.00"])
    average_duration_minutes: int = Field(default=60, ge=0, examples=[60])
    user_modification_id: int = Field(default=1)


class ServiceUpdateDTO(BaseModel):
    description: str | None = None
    price: Decimal | None = None
    average_duration_minutes: int | None = Field(default=None, ge=0)
    user_modification_id: int | None = None
    flag_active: bool | None = None
