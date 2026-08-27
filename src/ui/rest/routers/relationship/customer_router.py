from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.customer_dto import (
    CustomerCreateDTO,
    CustomerDetailDTO,
    CustomerDTO,
    CustomerFullCreateDTO,
    CustomerUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ui.rest.dependencies import get_for_manage_customer, require_admin

customer_router = APIRouter(
    prefix="/customer",
    tags=["customer"],
    dependencies=[Depends(require_admin)],
)


@customer_router.post("/", response_model=CustomerDTO)
def create_customer(
    customer: CustomerFullCreateDTO,
    use_case: ForManageCustomer = Depends(get_for_manage_customer),
):
    try:
        return use_case.create_customer(customer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@customer_router.post("/from-cpf", response_model=CustomerDTO)
def create_customer_only_cpf(
    customer: CustomerCreateDTO,
    use_case: ForManageCustomer = Depends(get_for_manage_customer),
):
    try:
        return use_case.create_customer_only_cpf(customer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@customer_router.get("/{customer_id}", response_model=CustomerDetailDTO)
def read_customer(
    customer_id: int,
    use_case: ForManageCustomer = Depends(get_for_manage_customer),
):
    try:
        return use_case.read_customer(customer_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@customer_router.patch("/{customer_id}", response_model=CustomerDTO)
def update_customer(
    customer_id: int,
    customer: CustomerUpdateDTO,
    use_case: ForManageCustomer = Depends(get_for_manage_customer),
):
    try:
        return use_case.update_customer(customer_id, customer)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@customer_router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    use_case: ForManageCustomer = Depends(get_for_manage_customer),
):
    try:
        return use_case.delete_customer(customer_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
