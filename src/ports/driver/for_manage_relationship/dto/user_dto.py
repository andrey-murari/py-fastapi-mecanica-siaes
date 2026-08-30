from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.domain.relationship.value_objects.user_type import UserType


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    user_type: UserType
    login: str
    password: str
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class UserCreateDTO(BaseModel):
    user_type: UserType
    person_id: str
    complete_name: str
    user_modification_id: int = Field(default=1)
