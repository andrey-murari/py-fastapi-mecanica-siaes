from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.ports.driver.for_manage_relationship.dto.person_dto import PersonDTO, PersonCreateDTO, PersonUpdateDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ui.rest.dependencies import get_for_manage_person
people_router = APIRouter(prefix="/people", tags=["people"])


@people_router.post("/", response_model=PersonDTO)
def create_person(
    person: PersonCreateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.create_person(person)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@people_router.get("/{person_id}", response_model=PersonDTO)
def read_customer(
    person_id: int,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.read_person(person_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@people_router.patch("/{person_id}", response_model=PersonDTO)
def update_person(
    person_id: int,
    person: PersonUpdateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.update_person(person_id, person)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@people_router.delete("/{person_id}")
def delete_customer(
    person_id: int,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.delete_person(person_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
