from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.domain.relationship.value_objects.contact_type import ContactType


class PersonDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_id: str
    complete_name: str
    user_id: str | None = None
    user_modification_id: int
    flag_customer: bool = Field(default=False)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)


class PersonCreateDTO(BaseModel):
    person_id: str = Field(examples=["52998224725"])
    complete_name: str = Field(examples=["Andrey Murari"])
    user_modification_id: int = Field(default=1)
    flag_active: bool = True


class PersonUpdateDTO(BaseModel):
    complete_name: str | None = None
    user_id: str | None = None
    user_modification_id: int | None = None
    flag_active: bool | None = None


class PersonAddressDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_address_id: int | None = None
    person_id: str
    cep_id: str
    number: str
    complement: str | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class PersonAddressCreateDTO(BaseModel):
    number: str
    complement: str | None = None


class PersonAddressViewDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_address_id: int | None = None
    cep_id: str
    number: str
    complement: str | None = None
    flag_active: bool = True


class PersonContactDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    contact_id: int | None = None
    person_id: str
    contact_type: ContactType
    value: str
    flag_preferred: bool = False
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class PersonContactCreateDTO(BaseModel):
    contact_type: ContactType
    value: str = Field(examples=["11987654321"])
    flag_preferred: bool = False
    user_modification_id: int = Field(default=1)
    flag_active: bool = True


class PersonContactUpdateDTO(BaseModel):
    contact_type: ContactType | None = None
    value: str | None = None
    flag_preferred: bool | None = None
    user_modification_id: int | None = None
    flag_active: bool | None = None


class PersonContactViewDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    contact_id: int | None = None
    contact_type: ContactType
    value: str
    flag_preferred: bool = False
    flag_active: bool = True


class PersonDetailDTO(PersonDTO):
    addresses: list[PersonAddressViewDTO] = Field(default_factory=list)
    contacts: list[PersonContactViewDTO] = Field(default_factory=list)
