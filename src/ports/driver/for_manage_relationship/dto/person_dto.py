from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PersonDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cpf: str = Field(min_length=11, max_length=11)
    complete_name: str = Field(min_length=3, max_length=255)
    user_id: int
    user_modification_id: int
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)


class PersonCreateDTO(BaseModel):
    cpf: str = Field(min_length=11, max_length=11)
    complete_name: str = Field(min_length=3, max_length=255)
    user_id: int
    user_modification_id: int
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)


class PersonUpdateDTO(BaseModel):
    complete_name: str | None = Field(default=None, min_length=3, max_length=255)
    user_id: int | None = Field(default=None, gt=0)
    user_modification_id: int | None = Field(default=None, gt=0)
    flag_active: bool | None = None
    modification_date: datetime | None = None


class PersonAddressDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_address_id: int | None = None
    cpf: str = Field(min_length=11, max_length=11)
    cep_id: str = Field(min_length=8, max_length=8)
    number: str = Field(min_length=1, max_length=20)
    complement: str | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class PersonAddressCreateDTO(BaseModel):
    number: str = Field(min_length=1, max_length=20)
    complement: str | None = None
