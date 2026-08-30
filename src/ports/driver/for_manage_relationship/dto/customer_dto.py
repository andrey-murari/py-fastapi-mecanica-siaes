from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.domain.relationship.value_objects.fuel_type import FuelType
from src.ports.driver.for_manage_relationship.dto.address_dto import AddressInputDTO
from src.ports.driver.for_manage_relationship.dto.person_dto import PersonAddressCreateDTO


class CustomerDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_id: str = Field(min_length=11, max_length=14)
    complete_name: str
    user_id: str | None = None
    flag_customer: bool = Field(default=True)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class CustomerFullCreateDTO(BaseModel):
    person_id: str = Field(examples=["52998224725"])
    complete_name: str = Field(min_length=3, max_length=255)
    user_modification_id: int = Field(default=1)
    address: AddressInputDTO
    person_address: PersonAddressCreateDTO
    flag_active: bool = True


class CustomerUpdateDTO(BaseModel):
    flag_active: bool | None = None


class CustomerPersonAddressDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_address_id: int | None = None
    number: str
    complement: str | None = None
    flag_active: bool = True


class CustomerAddressDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cep_id: str
    street: str = ""
    neighborhood: str = ""
    city: str
    state: str
    flag_active: bool = True
    person_address: CustomerPersonAddressDTO | None = None


class CustomerVehicleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle_id: int | None = None
    model: str
    brand: str
    manufacture_year: str
    model_year: str
    engine: str
    fuel_type: FuelType
    plate: str
    color: str
    description: str | None = None
    flag_active: bool = True


class CustomerDetailDTO(CustomerDTO):
    addresses: list[CustomerAddressDTO] = Field(default_factory=list)
    vehicles: list[CustomerVehicleDTO] = Field(default_factory=list)
