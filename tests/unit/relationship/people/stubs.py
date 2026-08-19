from src.domain.customers_and_services.relationship.entities import People
from src.domain.customers_and_services.relationship.entities import User
from src.domain.customers_and_services.relationship.entities import Address
from src.domain.customers_and_services.relationship.entities import Customer
from src.domain.customers_and_services.relationship.value_objects.user_type import UserType
from datetime import datetime

def stub_address():
    return Address(
        address_id=1,
        address="Rua das Flores, 123",
        number="123",
        complement="Apto 101",
        neighborhood="Jardim",
        city="São Paulo",
        state="SP",
        zip_code="1234567890",
        country="Brasil",
        user_id=1,
        user_modification_id=1,
        flag_active=True,
        insertion_date=datetime.now(),
        modification_date=datetime.now()
    )

def stub_person():
    return People(
        cpf="1234567890",
        complete_name="Andrey Murari",
        cep_id=35052130,
        user_id=1,
        user_modification_id=1,
        flag_active=True,
        insertion_date=datetime.now(),
        modification_date=datetime.now()
    )

def stub_user():
    return User(
        user_id=1,
        user_type=UserType.ADMIN,
        login="andrey.murari",
        password="123456",
        user_modification_id=1,
        flag_active=True,
        insertion_date=datetime.now(),
        modification_date=datetime.now()
    )

def stub_customer():
    return Customer(
        customer_id=1,
        people=stub_person(),
        flag_active=True,
        insertion_date=datetime.now(),
        modification_date=datetime.now()
    )