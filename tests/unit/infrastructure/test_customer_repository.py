from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.infrastructure.repository.models.customer_repository import (
    Base,
    CustomerModel,
    PeopleModel,
    SqlCustomerRepository,
)


def test_get_by_id_returns_domain_customer() -> None:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    now = datetime.now()
    with Session(engine) as session:
        session.add(
            PeopleModel(
                cpf="12345678901",
                complete_name="Andrey Murari",
                cep_id=1,
                user_id=1,
                user_modification_id=1,
                flag_active=True,
                insertion_date=now,
                modification_date=now,
            )
        )
        session.add(
            CustomerModel(
                customer_id=1,
                cpf="12345678901",
                flag_active=True,
                insertion_date=now,
                modification_date=now,
            )
        )
        session.commit()
        customer = SqlCustomerRepository(session).get_by_id(1)

    assert customer is not None
    assert customer.customer_id == 1
    assert customer.people.cpf == "12345678901"
    assert customer.flag_active is True
