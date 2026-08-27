import pytest
from pydantic import ValidationError

from src.domain.relationship.entities import Customer
from tests.unit.relationship.people.stubs import stub_customer


def test_create_customer():
    customer = stub_customer()
    assert customer.customer_id == 1
    assert customer.cpf == "52998224725"
    assert customer.flag_active is True


def test_customer_cpf_must_be_valid():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        Customer(customer_id=1, cpf="12345678912")


def test_customer_cpf_must_have_eleven_digits():
    with pytest.raises(ValidationError):
        Customer(customer_id=1, cpf="123456789")
