from datetime import datetime

import pytest
from pydantic import ValidationError

from domain.entities.Cliente import Cliente


@pytest.fixture
def cliente() -> Cliente:
    now = datetime.now()
    return Cliente(
        cliente_id=1,
        cpf="12345678901",
        usuario_modificacao_id=1,
        flag_ativo=True,
        data_insercao=now,
        data_atualizacao=now,
    )


def test_criar_cliente_com_dados_validos(cliente: Cliente) -> None:
    assert cliente.cliente_id == 1
    assert cliente.cpf == "12345678901"
    assert cliente.usuario_modificacao_id == 1
    assert cliente.flag_ativo is True
    assert isinstance(cliente.data_insercao, datetime)
    assert isinstance(cliente.data_atualizacao, datetime)


def test_cliente_model_dump_json(cliente: Cliente) -> None:
    payload = cliente.model_dump_json()

    assert '"cpf":"12345678901"' in payload
    assert '"flag_ativo":true' in payload
    assert '"cliente_id":1' in payload


def test_criar_cliente_sem_cpf_levanta_validation_error() -> None:
    with pytest.raises(ValidationError):
        Cliente(cpf=None)  # type: ignore[arg-type]
