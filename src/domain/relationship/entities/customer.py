from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.relationship.entities.person import Person


class Customer(BaseModel):
    """Pydantic model for customer to assert data validation"""
    model_config = ConfigDict(from_attributes=True)

    customer_id: int | None = None
    cpf: str = Field(min_length=11, max_length=11)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @field_validator("cpf", mode="before")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        return Person.validate_cpf(value)
