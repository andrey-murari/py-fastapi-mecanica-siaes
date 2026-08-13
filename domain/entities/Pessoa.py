from datetime import datetime

from pydantic import BaseModel


class Pessoa(BaseModel):
    cpf: str
    nome_completo: str
    cep_id: int | None = None
    usuario_id: int | None = None
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
