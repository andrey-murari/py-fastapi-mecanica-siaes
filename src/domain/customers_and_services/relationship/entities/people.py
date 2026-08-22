from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from src.domain.customers_and_services.relationship.value_objects.gender import Gender
from src.domain.customers_and_services.relationship.value_objects.user_type import UserType


class People(BaseModel):
    cpf: str = Field(min_length=11, max_length=11)
    complete_name: str = Field(min_length=3, max_length=255)
    cep_id: int = Field(gt=0)
    user_id: int
    user_modification_id: int
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)

    @field_validator('complete_name')
    @classmethod
    def validate_complete_name_number(cls, name: str) -> str:
        if any(char.isdigit() for char in name):
            raise ValueError("Complete name must not contain numbers")
        return name


class PeopleAddress(BaseModel):
    """"""
    people_address_id: int
    cpf: int
    postal_code: int
    number: int
    complement: str


class User(BaseModel):
    user_id: int
    user_type: UserType
    login: str
    password: str
    user_modification_id: int
    flag_active: bool
    insertion_date: datetime
    modification_date: datetime
