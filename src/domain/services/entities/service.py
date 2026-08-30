from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Service(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    service_id: int | None = None
    description: str = Field(min_length=3, max_length=255)
    price: Decimal = Field(ge=0)
    average_duration_minutes: int = Field(default=60, ge=0)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value: str) -> str:
        description = str(value).strip()
        if not description:
            raise ValueError("Description must not be empty")
        return description
