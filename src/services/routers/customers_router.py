from datetime import datetime
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel

from src.domain.customers_and_services.relationship.entities import Address, Customer, People
from src.infrastructure.repository.models.addresses_repository import AddressRepository
from src.infrastructure.repository.models.customer_repository import CustomerRepository
from src.infrastructure.repository.models.people_repository import PeopleRepository
from src.infrastructure.viacep_client import ViaCepClient
from src.services.dependencies import SessionDep

router = APIRouter(prefix="/customers", tags=["customers"])
viacep_client = ViaCepClient()


class CustomerUpdate(SQLModel):
    cpf: str | None = Field(default=None, min_length=11, max_length=11)
    flag_active: bool | None = None


def require_person_by_cpf(session: Session, cpf: str) -> PeopleRepository:
    person = session.get(PeopleRepository, cpf)
    if not person:
        raise HTTPException(status_code=400, detail="CPF not found in people table")
    return person


def get_or_create_person(session: Session, people: People) -> PeopleRepository:
    person = session.get(PeopleRepository, people.cpf)
    if person is None:
        person = PeopleRepository(people)
        session.add(person)
        session.flush()
    return person


def get_or_create_address(session: Session, address: Address) -> AddressRepository:
    stored = session.get(AddressRepository, address.cep_id)
    if stored is None:
        stored = AddressRepository(address)
        session.add(stored)
        session.commit()
        session.refresh(stored)
    return stored


@router.get("/cep/{cep}", response_model=Address)
def lookup_cep(cep: str, session: SessionDep) -> Address:
    try:
        payload = viacep_client.fetch(cep)
        address = Address.from_viacep(payload)
    except ValueError as exc:
        detail = str(exc)
        status_code = 404 if "not found" in detail.lower() else 400
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="ViaCEP is unavailable") from exc
    return get_or_create_address(session, address)


@router.post("/", response_model=Customer)
def create_customer(customer: Customer, people: People, session: SessionDep):
    qry_customer = session.get(CustomerRepository, customer.customer_id)
    if qry_customer:
        raise HTTPException(status_code=400, detail="User already exists")
    if people.cpf != customer.cpf:
        raise HTTPException(status_code=400, detail="Customer CPF does not match people CPF")
    get_or_create_person(session, people)
    db_cust = CustomerRepository(customer)
    session.add(db_cust)
    session.commit()
    session.refresh(db_cust)
    return db_cust


@router.get("/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, session: SessionDep) -> Customer:
    result = session.get(CustomerRepository, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result


@router.patch("/{customer_id}", response_model=Customer)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    session: SessionDep
) -> Customer:
    query_result = session.get(CustomerRepository, customer_id)
    if not query_result:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_data = customer.model_dump(exclude_unset=True)
    if "cpf" in customer_data:
        require_person_by_cpf(session, customer_data["cpf"])
    for key, value in customer_data.items():
        setattr(query_result, key, value)
    query_result.modification_date = datetime.now()
    session.add(query_result)
    session.commit()
    session.refresh(query_result)
    return query_result


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, session: SessionDep) -> dict[str, Any]:
    customer = session.get(CustomerRepository, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"ok": True}
