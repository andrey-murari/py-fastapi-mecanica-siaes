from src.domain.customers_and_services.relationship.entities.people import People

def test_create_numeric_name_person():
    person = People(cpf='12345678901',
                    complete_name='andrey',
                    cep_id='05040000',
                    user_id=1,
                    user_modification_id=2)

    print(person)

    assert person is not None
    assert person.complete_name is not None
    assert person.cep_id is not None
    assert person.user_id is not None
