from src.domain.customers_and_services.relationship.entities.people import People
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Customer(BaseModel):
    """Pydantic model for customer to assert data validation"""
    customer_id: int = Field(min_length=1, max_length=100)
    people: People
    flag_active: bool = True
    insertion_date: datetime = Field(default=datetime.now())
    modification_date: datetime
    