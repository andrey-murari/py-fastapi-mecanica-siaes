from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime


class Customer(BaseModel):
    """Pydantic model for customer to assert data validation"""
    model_config = ConfigDict(from_attributes=True)

    customer_id: int = Field(gt=0)
    cpf: str = Field(min_length=11, max_length=11)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default=datetime.now())
    modification_date: datetime | None = Field(default=None)

    @field_validator('cpf')
    @classmethod
    def validate_cpf_numeric(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("CPF must contain only numbers")
        return value