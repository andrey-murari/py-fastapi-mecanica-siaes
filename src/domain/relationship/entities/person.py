from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.relationship.entities.address import Address
from src.domain.relationship.value_objects.user_type import UserType


class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cpf: str = Field(min_length=11, max_length=11)
    complete_name: str = Field(min_length=3, max_length=255)
    user_id: int
    user_modification_id: int
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)

    @field_validator("cpf", mode="before")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        digits = "".join(char for char in str(value) if char.isdigit())
        if len(digits) != 11:
            raise ValueError("CPF must contain exactly 11 digits")
        if len(set(digits)) == 1:
            raise ValueError("CPF cannot have all digits equal")
        numbers = [int(digit) for digit in digits]
        if cls._cpf_check_digit(numbers[:9]) != numbers[9]:
            raise ValueError("Invalid CPF")
        if cls._cpf_check_digit(numbers[:10]) != numbers[10]:
            raise ValueError("Invalid CPF")
        return digits

    @staticmethod
    def _cpf_check_digit(numbers: list[int]) -> int:
        weights = range(len(numbers) + 1, 1, -1)
        total = sum(digit * weight for digit, weight in zip(numbers, weights))
        remainder = (total * 10) % 11
        return 0 if remainder == 10 else remainder

    @field_validator("complete_name")
    @classmethod
    def validate_complete_name_number(cls, name: str) -> str:
        if any(char.isdigit() for char in name):
            raise ValueError("Complete name must not contain numbers")
        return name


class PersonAddress(BaseModel):
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

    @field_validator("cpf", mode="before")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        return Person.validate_cpf(value)

    @field_validator("cep_id", mode="before")
    @classmethod
    def validate_cep(cls, value: str) -> str:
        return Address.validate_cep_numeric(value)


class User(BaseModel):
    user_id: int
    user_type: UserType
    login: str
    password: str
    user_modification_id: int
    flag_active: bool
    insertion_date: datetime
    modification_date: datetime
