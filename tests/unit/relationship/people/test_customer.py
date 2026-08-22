import pytest
from pydantic import ValidationError

from src.domain.customers_and_services.relationship.entities import Customer
from tests.unit.relationship.people.stubs import stub_customer


def test_create_customer():
    customer = stub_customer()
    assert customer.customer_id == 1
    assert customer.cpf == "12345678901"
    assert customer.flag_active is True


def test_customer_cpf_must_be_numeric():
    with pytest.raises(ValidationError, match="only numbers"):
        Customer(customer_id=1, cpf="1234567890A")


def test_customer_cpf_must_have_eleven_digits():
    with pytest.raises(ValidationError):
        Customer(customer_id=1, cpf="123456789")


def test_customer_id_must_be_positive():
    with pytest.raises(ValidationError):
        Customer(customer_id=0, cpf="12345678901")
