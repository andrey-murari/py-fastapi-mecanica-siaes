from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PartDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    part_id: int | None = None
    description: str
    brand: str
    manufacturer: str
    unit_price: Decimal
    available_quantity: int = Field(default=0)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class PartCreateDTO(BaseModel):
    description: str = Field(examples=["Filtro de oleo"])
    brand: str = Field(examples=["Bosch"])
    manufacturer: str = Field(examples=["Bosch do Brasil"])
    unit_price: Decimal = Field(examples=["89.90"])
    user_modification_id: int = Field(default=1)


class PartUpdateDTO(BaseModel):
    description: str | None = None
    brand: str | None = None
    manufacturer: str | None = None
    unit_price: Decimal | None = None
    user_modification_id: int | None = None
    flag_active: bool | None = None
