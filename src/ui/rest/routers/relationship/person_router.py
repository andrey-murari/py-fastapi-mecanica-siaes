from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.person_dto import PersonCreateDTO, PersonDTO, PersonUpdateDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ui.rest.dependencies import get_for_manage_person, require_admin

person_router = APIRouter(
    prefix="/person",
    tags=["person"],
    dependencies=[Depends(require_admin)],
)


@person_router.post("/", response_model=PersonDTO)
def create_person(
    person: PersonCreateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.create_person(person)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@person_router.get("/{person_id}", response_model=PersonDTO)
def read_person(
    person_id: int,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.read_person(person_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@person_router.patch("/{person_id}", response_model=PersonDTO)
def update_person(
    person_id: int,
    person: PersonUpdateDTO,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.update_person(person_id, person)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@person_router.delete("/{person_id}")
def delete_person(
    person_id: int,
    use_case: ForManagePerson = Depends(get_for_manage_person),
):
    try:
        return use_case.delete_person(person_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
