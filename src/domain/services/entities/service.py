from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class Service(BaseModel):
    service_id: int
    description: str = Field(min_length=3, max_length=255)
    price: Decimal = Field(ge=0)
    user_modification_id: int
    flag_active: bool
    insertion_date: datetime
    modification_date: datetime | None