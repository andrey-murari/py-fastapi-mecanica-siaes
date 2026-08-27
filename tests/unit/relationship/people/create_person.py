import pytest
from pydantic import ValidationError

from src.domain.relationship.entities import Person
from tests.unit.relationship.people.stubs import stub_person


def test_create_person():
    person = stub_person()
    assert person.cpf == "52998224725"
    assert person.complete_name == "Andrey Murari"


def test_people_rejects_digits_in_complete_name():
    with pytest.raises(ValidationError, match="must not contain numbers"):
        Person(
            cpf="52998224725",
            complete_name="Andrey123",
            user_id=1,
            user_modification_id=1,
        )


def test_people_accepts_name_without_digits():
    person = Person(
        cpf="52998224725",
        complete_name="andrey",
        user_id=1,
        user_modification_id=2,
    )
    assert person.complete_name == "andrey"
