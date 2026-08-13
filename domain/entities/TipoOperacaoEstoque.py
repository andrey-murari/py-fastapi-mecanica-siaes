from datetime import datetime

from pydantic import BaseModel


class TipoOperacaoEstoque(BaseModel):
    tipo_operacao_estoque_id: int | None = None
    descricao_operacao: str
    usuario_modificacao_id: int | None = None
    flag_ativo: bool = True
    data_insercao: datetime | None = None
    data_atualizacao: datetime | None = None
