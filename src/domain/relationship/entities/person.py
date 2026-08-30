from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.relationship.entities.address import Address
from src.domain.relationship.value_objects.user_type import UserType


class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_id: str = Field(min_length=11, max_length=14)
    complete_name: str = Field(min_length=3, max_length=255)
    user_id: str | None = None
    user_modification_id: int
    flag_customer: bool = Field(default=False)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)

    @field_validator("person_id", mode="before")
    @classmethod
    def validate_person_id(cls, value: str) -> str:
        digits = "".join(char for char in str(value) if char.isdigit())
        if len(digits) == 11:
            return cls._validate_cpf(digits)
        if len(digits) == 14:
            return cls._validate_cnpj(digits)
        raise ValueError("Must be a valid CPF (11 digits) or CNPJ (14 digits)")

    @classmethod
    def _validate_cpf(cls, digits: str) -> str:
        if len(set(digits)) == 1:
            raise ValueError("CPF cannot have all digits equal")
        numbers = [int(digit) for digit in digits]
        if cls._cpf_check_digit(numbers[:9]) != numbers[9]:
            raise ValueError("Invalid CPF")
        if cls._cpf_check_digit(numbers[:10]) != numbers[10]:
            raise ValueError("Invalid CPF")
        return digits

    @classmethod
    def _validate_cnpj(cls, digits: str) -> str:
        if len(set(digits)) == 1:
            raise ValueError("CNPJ cannot have all digits equal")
        numbers = [int(digit) for digit in digits]
        if cls._cnpj_check_digit(numbers[:12]) != numbers[12]:
            raise ValueError("Invalid CNPJ")
        if cls._cnpj_check_digit(numbers[:13]) != numbers[13]:
            raise ValueError("Invalid CNPJ")
        return digits

    @staticmethod
    def _cpf_check_digit(numbers: list[int]) -> int:
        weights = range(len(numbers) + 1, 1, -1)
        total = sum(digit * weight for digit, weight in zip(numbers, weights))
        remainder = (total * 10) % 11
        return 0 if remainder == 10 else remainder

    @staticmethod
    def _cnpj_check_digit(numbers: list[int]) -> int:
        # Weights run 5..2 then 9..2, so they restart after the first four digits.
        weights = [(index % 8) + 2 for index in range(len(numbers) - 1, -1, -1)]
        total = sum(digit * weight for digit, weight in zip(numbers, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    @field_validator("complete_name")
    @classmethod
    def validate_complete_name_number(cls, name: str) -> str:
        if any(char.isdigit() for char in name):
            raise ValueError("Complete name must not contain numbers")
        return name


class PersonAddress(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    person_address_id: int | None = None
    person_id: str = Field(min_length=11, max_length=14)
    cep_id: str = Field(min_length=8, max_length=8)
    number: str = Field(min_length=1, max_length=20)
    complement: str | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @field_validator("person_id", mode="before")
    @classmethod
    def validate_person_id(cls, value: str) -> str:
        return Person.validate_person_id(value)

    @field_validator("cep_id", mode="before")
    @classmethod
    def validate_cep(cls, value: str) -> str:
        return Address.validate_cep_numeric(value)


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    user_type: UserType
    login: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=255)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @classmethod
    def credentials_for(cls, person_id: str, complete_name: str) -> tuple[str, str]:
        digits = "".join(char for char in str(person_id) if char.isdigit())
        initials = "".join(part[0] for part in complete_name.split() if part).upper()
        return digits, f"{initials}{digits[-4:]}"
