from pydantic import BaseModel
from datetime import date

class Customer(BaseModel):
    name: str
    age: int
    email: str
    birthday: date
