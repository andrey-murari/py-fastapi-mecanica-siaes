Feature: Consulta de cliente no sistema
  Como operador do sistema
  Quero consultar se um cliente possui cadastro
  Para saber se o CPF já está registrado

  Scenario: Cliente já cadastrado
    Given que o cliente já está cadastrado no sistema
    When efetuar consulta do cliente no sistema
    Then exibe que o cliente já possui cadastro

  Scenario: Cliente não cadastrado
    Given que o cliente não está cadastrado no sistema
    When efetuar consulta do cliente no sistema
    Then exibe que o cliente não possui cadastro
