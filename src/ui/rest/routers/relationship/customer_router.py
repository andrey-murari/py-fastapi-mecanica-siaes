from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.customer_dto import (
    CustomerDetailDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ui.rest.dependencies import get_for_manage_customer, require_admin
from src.ui.rest.http_responses import RESPONSES_400, RESPONSES_400_404

customer_router = APIRouter(
    prefix="/customer",
    tags=["customer"],
    dependencies=[Depends(require_admin)],
)


def _raise_http(exc: ValueError) -> HTTPException:
    status_code = 404 if str(exc) == "Customer not found" else 400
    return HTTPException(status_code=status_code, detail=str(exc))


@customer_router.post("/", response_model=CustomerDTO, responses=RESPONSES_400)
def create_customer(
    customer: CustomerFullCreateDTO,
    use_case: Annotated[ForManageCustomer, Depends(get_for_manage_customer)],
):
    try:
        return use_case.create_customer(customer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@customer_router.get("/{person_id}", response_model=CustomerDetailDTO, responses=RESPONSES_400_404)
def read_customer(
    person_id: str,
    use_case: Annotated[ForManageCustomer, Depends(get_for_manage_customer)],
):
    try:
        return use_case.read_customer(person_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@customer_router.patch("/{person_id}", response_model=CustomerDTO, responses=RESPONSES_400_404)
def update_customer(
    person_id: str,
    customer: CustomerUpdateDTO,
    use_case: Annotated[ForManageCustomer, Depends(get_for_manage_customer)],
):
    try:
        return use_case.update_customer(person_id, customer)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@customer_router.delete("/{person_id}", responses=RESPONSES_400_404)
def delete_customer(
    person_id: str,
    use_case: Annotated[ForManageCustomer, Depends(get_for_manage_customer)],
):
    try:
        return use_case.delete_customer(person_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc
