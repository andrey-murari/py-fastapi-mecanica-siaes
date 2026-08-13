from datetime import datetime

from pydantic import BaseModel


class TipoContato(BaseModel):
    tipo_contato_id: int | None = None
    tipo_contato: str
    descricao: str | None = None
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
