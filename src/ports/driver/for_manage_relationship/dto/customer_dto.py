from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.ports.driver.for_manage_relationship.dto.address_dto import AddressInputDTO
from src.ports.driver.for_manage_relationship.dto.person_dto import PersonAddressCreateDTO


class CustomerDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int | None = None
    cpf: str = Field(min_length=11, max_length=11)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class CustomerCreateDTO(BaseModel):
    cpf: str = Field(min_length=11, max_length=11, examples=["52998224725"])


class CustomerFullCreateDTO(BaseModel):
    cpf: str = Field(min_length=11, max_length=11, examples=["52998224725"])
    complete_name: str = Field(min_length=3, max_length=255)
    user_id: int = Field(default=1)
    user_modification_id: int = Field(default=1)
    address: AddressInputDTO
    person_address: PersonAddressCreateDTO
    flag_active: bool = True


class CustomerUpdateDTO(BaseModel):
    flag_active: bool | None = None
