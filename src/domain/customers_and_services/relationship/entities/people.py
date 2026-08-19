from pydantic import BaseModel
from datetime import datetime
from src.domain.customers_and_services.relationship.value_objects.gender import Gender
from src.domain.customers_and_services.relationship.value_objects.user_type import UserType
from pydantic import Field


class People(BaseModel):
    cpf: str =Field(min_length=11, max_length=11)
    complete_name: str =Field(min_length=3, max_length=255)
    cep_id: int = Field(gt=0)
    user_id: int
    user_modification_id: int
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)


class User(BaseModel):
    user_id: int
    user_type: UserType
    login: str
    password: str
    user_modification_id: int
    flag_active: bool
    insertion_date: datetime
    modification_date: datetime

# I prefer to use ENUMS because this is an MVV pattern and the user type is a static value
# class UserType(BaseModel):
#     user_type_id: int
#     type: str
#     description: str
#     user_modification_id: int
#     flag_active: bool
#     insertion_date: datetime
#     modification_date: datetime