from datetime import datetime

from pydantic import BaseModel


class Endereco(BaseModel):
    cep_id: int | None = None
    logradouro: str
    bairro: str
    cidade: str
    uf: str
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
