from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Part(BaseModel):
    """Peca / insumo available in the workshop catalog."""

    model_config = ConfigDict(from_attributes=True)

    part_id: int | None = None
    description: str = Field(min_length=3, max_length=255)
    brand: str = Field(min_length=1, max_length=100)
    manufacturer: str = Field(min_length=1, max_length=100)
    unit_price: Decimal = Field(ge=0)
    available_quantity: int = Field(default=0, ge=0)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @field_validator("description", "brand", "manufacturer", mode="before")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        text = str(value).strip()
        if not text:
            raise ValueError("Value must not be empty")
        return text
