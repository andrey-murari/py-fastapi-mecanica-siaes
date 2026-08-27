from src.customers_and_services.relationship.application.customer_use_cases import (
    CustomerUseCases,
)
from src.ports.driver.for_manage_customer.customer import Customer
from src.ports.driver.for_manage_customer.for_manage_customer import ForManageCustomer
from src.ports.driving.for_get_address.for_get_address import ForGetAddress
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData
from src.ui.rest.routers.relationship.customer_router import create_customer, read_customer
from fastapi import HTTPException


def stub_viacep_payload() -> dict:
    return {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
    }


class FakeStorage(ForStoringData):
    def __init__(self) -> None:
        self.customers: dict[int, dict] = {}
        self.addresses: dict[str, dict] = {}

    def create_db_and_tables(self) -> None:
        return None

    def close(self) -> None:
        return None

    def get_customer(self, customer_id: int) -> dict | None:
        return self.customers.get(customer_id)

    def save_customer(self, customer: dict) -> dict:
        self.customers[customer["customer_id"]] = customer
        return customer

    def delete_customer(self, customer_id: int) -> None:
        self.customers.pop(customer_id, None)

    def get_address(self, cep_id: str) -> dict | None:
        return self.addresses.get(cep_id)

    def save_address(self, address: dict) -> dict:
        self.addresses[address["cep_id"]] = address
        return address


class FakeAddresses(ForGetAddress):
    def get_address_by_cep(self, cep: str) -> dict:
        if cep.replace("-", "") == "99999999":
            return {"erro": True}
        return stub_viacep_payload()


class _FakeUseCase(ForManageCustomer):
    def create_customer(self, customer: dict) -> Customer:
        return Customer.model_validate(customer)

    def read_customer(self, customer_id: int) -> Customer:
        raise ValueError("Customer not found")

    def update_customer(self, customer_id: int, customer: dict) -> Customer:
        raise ValueError("Customer not found")

    def delete_customer(self, customer_id: int) -> dict:
        raise ValueError("Customer not found")


def test_router_create_delegates_to_port():
    payload = Customer(customer_id=1, cpf="12345678901")
    result = create_customer(payload, use_case=_FakeUseCase())
    assert result.customer_id == 1
    assert result.cpf == "12345678901"


def test_router_read_maps_value_error_to_404():
    try:
        read_customer(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")


def test_use_case_create_and_read():
    use_case = CustomerUseCases(storage=FakeStorage(), addresses=FakeAddresses())
    created = use_case.create_customer({"customer_id": 1, "cpf": "12345678901"})
    assert use_case.read_customer(1).cpf == created.cpf


def test_use_case_rejects_duplicate():
    use_case = CustomerUseCases(storage=FakeStorage(), addresses=FakeAddresses())
    use_case.create_customer({"customer_id": 1, "cpf": "12345678901"})
    try:
        use_case.create_customer({"customer_id": 1, "cpf": "12345678901"})
    except ValueError as exc:
        assert str(exc) == "User already exists"
    else:
        raise AssertionError("expected ValueError")


def test_use_case_create_with_cep_saves_address():
    storage = FakeStorage()
    use_case = CustomerUseCases(storage=storage, addresses=FakeAddresses())
    use_case.create_customer({
        "customer_id": 1,
        "cpf": "12345678901",
        "cep": "01001000",
    })
    assert "01001000" in storage.addresses
    assert storage.addresses["01001000"]["city"] == "São Paulo"
