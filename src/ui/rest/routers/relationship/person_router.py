from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.person_dto import (
    PersonContactCreateDTO,
    PersonContactDTO,
    PersonContactUpdateDTO,
    PersonCreateDTO,
    PersonDetailDTO,
    PersonDTO,
    PersonUpdateDTO,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ui.rest.dependencies import get_for_manage_person, require_admin

person_router = APIRouter(
    prefix="/person",
    tags=["person"],
    dependencies=[Depends(require_admin)],
)

_NOT_FOUND_MESSAGES = frozenset({"Person not found", "Contact not found"})


def _raise_http(exc: ValueError) -> HTTPException:
    status_code = 404 if str(exc) in _NOT_FOUND_MESSAGES else 400
    return HTTPException(status_code=status_code, detail=str(exc))


@person_router.post("/", response_model=PersonDTO)
def create_person(
    person: PersonCreateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.create_person(person)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@person_router.get("/{cpf}", response_model=PersonDetailDTO)
def read_person(
    cpf: str,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.read_person(cpf)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@person_router.patch("/{cpf}", response_model=PersonDTO)
def update_person(
    cpf: str,
    person: PersonUpdateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.update_person(cpf, person)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@person_router.delete("/{cpf}")
def delete_person(
    cpf: str,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.delete_person(cpf)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@person_router.post("/{cpf}/contact", response_model=PersonContactDTO)
def create_contact(
    cpf: str,
    contact: PersonContactCreateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.create_contact(cpf, contact)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@person_router.get("/{cpf}/contact", response_model=list[PersonContactDTO])
def list_contacts(
    cpf: str,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.list_contacts(cpf)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@person_router.get("/{cpf}/contact/{contact_id}", response_model=PersonContactDTO)
def read_contact(
    cpf: str,
    contact_id: int,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.read_contact(cpf, contact_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@person_router.patch("/{cpf}/contact/{contact_id}", response_model=PersonContactDTO)
def update_contact(
    cpf: str,
    contact_id: int,
    contact: PersonContactUpdateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.update_contact(cpf, contact_id, contact)
    except ValueError as exc:
        raise _raise_http(exc) from exc


@person_router.delete("/{cpf}/contact/{contact_id}")
def delete_contact(
    cpf: str,
    contact_id: int,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.delete_contact(cpf, contact_id)
    except ValueError as exc:
        raise _raise_http(exc) from exc
