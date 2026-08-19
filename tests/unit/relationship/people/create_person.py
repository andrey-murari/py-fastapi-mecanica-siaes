from src.domain.customers_and_services.relationship.value_objects.user_type import UserType
from datetime import datetime
from tests.unit.relationship.people.stubs import stub_person
from src.domain.customers_and_services.relationship.entities import Customer

def test_create_customer():
    person = stub_person()
    customer = Customer(
        customer_id=1,
        people=person,
        flag_active=True,
        insertion_date=datetime.now(),
        modification_date=datetime.now()
    )
    assert customer.customer_id == 1
    assert customer.people.cpf == "1234567890"
    assert customer.people.complete_name == "Andrey Murari"
    assert customer.people.cep_id == 35052130