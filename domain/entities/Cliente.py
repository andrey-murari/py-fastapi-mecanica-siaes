from datetime import date
from pydantic import BaseModel

class Cliente(BaseModel):
    nome: str
    sobrenome: str
    email: str
    data_nascimento: date
