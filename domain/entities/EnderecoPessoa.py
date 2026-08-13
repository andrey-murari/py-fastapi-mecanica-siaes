from datetime import datetime

from pydantic import BaseModel


class EnderecoPessoa(BaseModel):
    endereco_pessoa_id: int | None = None
    cpf: str
    cep_id: int
    numero: str
    complemento: str | None = None
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
