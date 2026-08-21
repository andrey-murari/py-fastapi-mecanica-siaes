from pydantic import BaseModel, Field
from datetime import datetime

class Address(BaseModel):
    """Adress class"""
    cep_id: int = Field(min_length=8, max_length=8)
    street: str
    neighborhood: str
    city: str
    state: str
    user_modification_id: int
    flag_active: bool
    insertion_date: datetime = Field(default=datetime.now)
    modification_date: datetime | None
