from src.infrastructure.repository.models.addresses_repository import AddressRepository
from src.infrastructure.repository.models.customer_repository import CustomerRepository
from src.infrastructure.repository.models.people_repository import PeopleRepository
from tests.unit.relationship.people.stubs import stub_address, stub_customer, stub_person


def test_address_repository_maps_entity_fields():
    row = AddressRepository(stub_address())
    assert row.cep_id == "01001000"
    assert row.street == "Praça da Sé"
    assert row.neighborhood == "Sé"
    assert row.city == "São Paulo"
    assert row.state == "SP"


def test_people_repository_maps_cep_id_as_string():
    row = PeopleRepository(stub_person())
    assert row.cpf == "12345678901"
    assert row.complete_name == "Andrey Murari"
    assert row.cep_id == "35052130"


def test_customer_repository_maps_entity_fields():
    row = CustomerRepository(stub_customer())
    assert row.customer_id == 1
    assert row.cpf == "12345678901"
    assert row.flag_active is True
