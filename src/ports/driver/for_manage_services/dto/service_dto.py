from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class ServiceDTO(BaseModel):
    service_id: int
    description: str
    price: Decimal
    user_modification_id: int
    flag_active: bool
    insertion_date: datetime
    modification_date: datetime | None

class ServiceCreateDTO(BaseModel):
    description: str = Field(min_length=3, max_length=255)
    price: Decimal = Field(ge=0)

class ServiceUpdateDTO(BaseModel):
    description: str | None = None
    price: Decimal | None = None
    flag_active: bool | None = None
