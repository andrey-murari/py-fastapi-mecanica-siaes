from fastapi import HTTPException

from src.ports.driver.for_manage_relationship.dto.customer_dto import (
    CustomerCreateDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
)
from src.ports.driver.for_manage_relationship.dto.address_dto import AddressDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ui.rest.routers.relationship.customer_router import (
    create_customer,
    create_customer_only_cpf,
    read_customer,
)


class _FakeUseCase(ForManageCustomer):
    def create_customer(self, customer: CustomerFullCreateDTO) -> CustomerDTO:
        return CustomerDTO(customer_id=1, cpf="52998224725")

    def create_customer_only_cpf(self, customer: CustomerCreateDTO) -> CustomerDTO:
        if customer.cpf == "52998224725":
            return CustomerDTO(customer_id=2, cpf=customer.cpf)
        raise ValueError("Person not found")

    def read_customer(self, customer_id: int) -> CustomerDTO:
        raise ValueError("Customer not found")

    def update_customer(self, customer_id: int, customer: CustomerUpdateDTO) -> CustomerDTO:
        raise ValueError("Customer not found")

    def delete_customer(self, customer_id: int) -> dict:
        raise ValueError("Customer not found")

    def get_address_by_cep(self, cep: str) -> AddressDTO:
        raise ValueError("unused")


def test_router_create_from_cpf_delegates_to_port():
    result = create_customer_only_cpf(
        CustomerCreateDTO(cpf="52998224725"),
        use_case=_FakeUseCase(),
    )
    assert result.customer_id == 2
    assert result.cpf == "52998224725"


def test_router_create_from_cpf_maps_value_error_to_400():
    try:
        create_customer_only_cpf(
            CustomerCreateDTO(cpf="11144477735"),
            use_case=_FakeUseCase(),
        )
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Person not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_value_error_to_404():
    try:
        read_customer(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_create_accepts_full_payload():
    result = create_customer(
        CustomerFullCreateDTO.model_validate(
            {
                "cpf": "52998224725",
                "complete_name": "Andrey Murari",
                "address": {"cep_id": "01001000", "city": "São Paulo", "state": "SP"},
                "person_address": {"number": "100"},
            }
        ),
        use_case=_FakeUseCase(),
    )
    assert result.customer_id == 1
