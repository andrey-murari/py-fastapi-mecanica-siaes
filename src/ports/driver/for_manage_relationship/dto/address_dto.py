from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cep_id: str = Field(min_length=8, max_length=8)
    street: str = Field(default="")
    neighborhood: str = Field(default="")
    city: str
    state: str = Field(min_length=2, max_length=2)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = Field(default=None)

    @field_validator("cep_id", mode="before")
    @classmethod
    def validate_cep_numeric(cls, value: str) -> str:
        cep = str(value).replace("-", "").replace(" ", "")
        if not cep.isdigit() or len(cep) != 8:
            raise ValueError("CEP must contain exactly 8 digits")
        return cep


class AddressInputDTO(BaseModel):
    cep_id: str
    street: str | None = None
    neighborhood: str | None = None
    city: str | None = None
    state: str | None = None

    @field_validator("cep_id", mode="before")
    @classmethod
    def validate_cep_numeric(cls, value: str) -> str:
        cep = str(value).replace("-", "").replace(" ", "")
        if not cep.isdigit() or len(cep) != 8:
            raise ValueError("CEP must contain exactly 8 digits")
        return cep

class AddressCreateDTO(BaseModel):
    cep_id: str = Field(min_length=8, max_length=8, example="12345678")
    street: str = Field(min_length=3, max_length=150, example="Rua das Flores")
    neighborhood: str = Field(min_length=3, max_length=150, example="Bairro das Flores")
    city: str = Field(min_length=3, max_length=50, example="São Paulo")
    state: str = Field(min_length=2, max_length=2, example="SP")

class AddressUpdateDTO(BaseModel):
    street: str | None = Field(min_length=3, max_length=150, example="Rua das Flores")
    neighborhood: str | None = Field(min_length=3, max_length=150, example="Bairro das Flores")
    city: str | None = Field(min_length=3, max_length=50, example="São Paulo")
    state: str | None = Field(min_length=2, max_length=2, example="SP")
    flag_active: bool | None = Field(default=True)