from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Address(BaseModel):
    """Address filled from ViaCEP and persisted locally."""

    model_config = ConfigDict(from_attributes=True)

    cep_id: str = Field(min_length=8, max_length=8, example="12345678", description="Numero do CEP (apenas numeros)")
    street: str = Field(default="", max_length=150, example="Rua das Flores", description="Nome da rua")
    neighborhood: str = Field(default="", max_length=150, example="Bairro das Flores", description="Nome do bairro")
    city: str = Field(min_length=3, max_length=50, example="São Paulo", description="Nome da cidade")
    state: str = Field(min_length=2, max_length=2, example="SP", description="Nome do estado")
    user_modification_id: int = Field(default=1, description="ID do usuario que modificou o endereco")
    flag_active: bool = Field(default=True, description="Flag de ativacao do endereco")
    insertion_date: datetime = Field(default_factory=datetime.now, description="Data de insercao do endereco")
    modification_date: datetime | None = Field(default=None, description="Data de modificacao do endereco")

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
