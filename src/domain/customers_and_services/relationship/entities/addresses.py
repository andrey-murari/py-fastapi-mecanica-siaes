from pydantic import BaseModel
from datetime import datetime

class Address(BaseModel):
    cep_id: int
    street: str
    neighborhood: str
    city: str
    state: str
    user_modification_id: int
    flag_active: bool
    insertion_date: datetime
    modification_date: datetime
