from src.domain.customers_and_services.relationship.entities.people import People
from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    customer_id: int
    people: People
    flag_active: bool
    insertion_date: datetime
    modification_date: datetime
