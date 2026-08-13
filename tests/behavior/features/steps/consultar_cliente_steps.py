from behave import given, then, when

from domain.entities.Cliente import Cliente
from domain.use_cases.Consultar import ConsultarCliente


@given("que o cliente já está cadastrado no sistema")
def step_cliente_ja_cadastrado(context) -> None:
    context.cpf = "12345678901"
    context.consultar = ConsultarCliente(
        [
            Cliente(
                cpf=context.cpf,
                usuario_modificacao_id=1,
            )
        ]
    )


@given("que o cliente não está cadastrado no sistema")
def step_cliente_nao_cadastrado(context) -> None:
    context.cpf = "98765432100"
    context.consultar = ConsultarCliente([])


@when("efetuar consulta do cliente no sistema")
def step_efetuar_consulta(context) -> None:
    context.resultado = context.consultar.executar_consulta(context.cpf)


@then("exibe que o cliente já possui cadastro")
def step_exibe_ja_possui_cadastro(context) -> None:
    assert context.resultado == "o cliente já possui cadastro"


@then("exibe que o cliente não possui cadastro")
def step_exibe_nao_possui_cadastro(context) -> None:
    assert context.resultado == "o cliente não possui cadastro"
