from src.domain.relationship.entities.person import Person


def test_create_numeric_name_person():
    person = Person(
        cpf="52998224725",
        complete_name="andrey",
        user_id=1,
        user_modification_id=2,
    )

    assert person is not None
    assert person.complete_name is not None
    assert person.user_id is not None
