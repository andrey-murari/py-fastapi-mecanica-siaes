from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Address(BaseModel):
    """Address filled from ViaCEP and persisted locally."""

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

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        return value.upper()

    @classmethod
    def from_viacep(cls, payload: dict[str, Any], *, user_modification_id: int = 1) -> "Address":
        if payload.get("erro") in (True, "true"):
            raise ValueError("CEP not found on ViaCEP")
        address = cls(
            cep_id=str(payload.get("cep", "")),
            street=payload.get("logradouro") or "",
            neighborhood=payload.get("bairro") or "",
            city=payload.get("localidade") or "",
            state=payload.get("uf") or "",
            user_modification_id=user_modification_id,
        )
        address.validate_viacep_response(payload)
        return address

    def validate_viacep_response(self, payload: dict[str, Any]) -> None:
        if payload.get("erro") in (True, "true"):
            raise ValueError("CEP not found on ViaCEP")
        returned_cep = str(payload.get("cep", "")).replace("-", "").replace(" ", "")
        if returned_cep != self.cep_id:
            raise ValueError("CEP returned by ViaCEP does not match the address")
        if not self.city or not self.state:
            raise ValueError("ViaCEP response is missing city or state")
