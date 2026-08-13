from datetime import datetime

from pydantic import BaseModel


class ContatoPessoa(BaseModel):
    contato_pessoa_id: int | None = None
    cpf: str
    tipo_contato_id: int
    valor_contato: str
    flag_preferencial: bool = False
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
