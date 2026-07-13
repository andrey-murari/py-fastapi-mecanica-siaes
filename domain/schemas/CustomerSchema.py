from pydantic import BaseModel
from datetime import date

class CustomerSchema (BaseModel):
    name: str
    age: int
    email: str
    birthday: date