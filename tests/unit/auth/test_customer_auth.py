from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.ports.driver.for_authenticate.dto import AdminIdentityDTO, LoginDTO, TokenDTO
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ports.driver.for_manage_relationship.dto.customer_dto import (
    CustomerCreateDTO,
    CustomerDetailDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
)
from src.ports.driver.for_manage_relationship.dto.address_dto import AddressDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ui.rest.dependencies import set_for_authenticate, set_for_manage_customer
from src.ui.rest.routers.relationship.customer_router import customer_router


class _FakeAuth(ForAuthenticate):
    def login(self, credentials: LoginDTO) -> TokenDTO:
        raise AssertionError("unused")

    def current_admin(self, token: str) -> AdminIdentityDTO:
        raise ValueError("Invalid token")


class _FakeCustomer(ForManageCustomer):
    def create_customer(self, customer: CustomerFullCreateDTO) -> CustomerDTO:
        raise AssertionError("unused")

    def create_customer_only_cpf(self, customer: CustomerCreateDTO) -> CustomerDTO:
        raise AssertionError("unused")

    def read_customer(self, customer_id: int) -> CustomerDetailDTO:
        raise AssertionError("should not run without auth")

    def update_customer(self, customer_id: int, customer: CustomerUpdateDTO) -> CustomerDTO:
        raise AssertionError("unused")

    def delete_customer(self, customer_id: int) -> dict:
        raise AssertionError("unused")

    def get_address_by_cep(self, cep: str) -> AddressDTO:
        raise AssertionError("unused")


def test_customer_read_without_token_returns_401():
    set_for_authenticate(_FakeAuth())
    set_for_manage_customer(_FakeCustomer())
    app = FastAPI()
    app.include_router(customer_router)
    client = TestClient(app)

    response = client.get("/customer/1")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
