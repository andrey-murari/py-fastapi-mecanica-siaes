from fastapi import HTTPException

from src.ports.driver.for_manage_relationship.dto.customer_dto import (
    CustomerDetailDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ui.rest.routers.relationship.customer_router import (
    create_customer,
    delete_customer,
    read_customer,
    update_customer,
)

VALID_CPF = "52998224725"
UNKNOWN_CPF = "11144477735"


def _customer(person_id: str = VALID_CPF) -> CustomerDTO:
    return CustomerDTO(person_id=person_id, complete_name="Andrey Murari", user_id=person_id)


class _FakeUseCase(ForManageCustomer):
    def create_customer(self, customer: CustomerFullCreateDTO) -> CustomerDTO:
        if customer.person_id == UNKNOWN_CPF:
            raise ValueError("Person already exists")
        return _customer(customer.person_id)

    def read_customer(self, person_id: str) -> CustomerDetailDTO:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Customer not found")
        if person_id == "123":
            raise ValueError("Invalid CPF")
        return CustomerDetailDTO(**_customer(person_id).model_dump())

    def update_customer(self, person_id: str, customer: CustomerUpdateDTO) -> CustomerDTO:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Customer not found")
        return _customer(person_id).model_copy(update={"flag_active": customer.flag_active})

    def delete_customer(self, person_id: str) -> dict:
        if person_id == UNKNOWN_CPF:
            raise ValueError("Customer not found")
        return {"ok": True}


def _full_payload(person_id: str = VALID_CPF) -> CustomerFullCreateDTO:
    return CustomerFullCreateDTO.model_validate(
        {
            "person_id": person_id,
            "complete_name": "Andrey Murari",
            "address": {"cep_id": "01001000", "city": "São Paulo", "state": "SP"},
            "person_address": {"number": "100"},
        }
    )


def test_router_create_accepts_full_payload():
    result = create_customer(_full_payload(), use_case=_FakeUseCase())
    assert result.person_id == VALID_CPF
    assert result.flag_customer is True


def test_router_create_maps_value_error_to_400():
    try:
        create_customer(_full_payload(UNKNOWN_CPF), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Person already exists"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_delegates_to_port():
    result = read_customer(VALID_CPF, use_case=_FakeUseCase())
    assert result.person_id == VALID_CPF


def test_router_read_maps_customer_not_found_to_404():
    try:
        read_customer(UNKNOWN_CPF, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_invalid_person_id_to_400():
    try:
        read_customer("123", use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Invalid CPF"
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_delegates_to_port():
    result = update_customer(
        VALID_CPF,
        CustomerUpdateDTO(flag_active=False),
        use_case=_FakeUseCase(),
    )
    assert result.flag_active is False


def test_router_delete_maps_value_error_to_404():
    try:
        delete_customer(UNKNOWN_CPF, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Customer not found"
    else:
        raise AssertionError("expected HTTPException")
