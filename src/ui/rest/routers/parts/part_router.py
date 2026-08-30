from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_parts.dto.part_dto import (
    PartCreateDTO,
    PartDTO,
    PartUpdateDTO,
)
from src.ports.driver.for_manage_parts.interfaces.for_manage_part import ForManagePart
from src.ui.rest.dependencies import get_for_manage_part, require_admin
from src.ui.rest.http_responses import RESPONSES_400, RESPONSES_400_404, RESPONSES_404

part_router = APIRouter(
    prefix="/part",
    tags=["part"],
    dependencies=[Depends(require_admin)],
)


@part_router.post("/", response_model=PartDTO, responses=RESPONSES_400)
def create_part(
    part: PartCreateDTO,
    use_case: Annotated[ForManagePart, Depends(get_for_manage_part)],
):
    try:
        return use_case.create_part(part)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@part_router.get("/{part_id}", response_model=PartDTO, responses=RESPONSES_404)
def read_part(
    part_id: int,
    use_case: Annotated[ForManagePart, Depends(get_for_manage_part)],
):
    try:
        return use_case.read_part(part_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@part_router.patch("/{part_id}", response_model=PartDTO, responses=RESPONSES_400_404)
def update_part(
    part_id: int,
    part: PartUpdateDTO,
    use_case: Annotated[ForManagePart, Depends(get_for_manage_part)],
):
    try:
        return use_case.update_part(part_id, part)
    except ValueError as exc:
        status_code = 404 if str(exc) == "Part not found" else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@part_router.delete("/{part_id}", responses=RESPONSES_404)
def delete_part(
    part_id: int,
    use_case: Annotated[ForManagePart, Depends(get_for_manage_part)],
):
    try:
        return use_case.delete_part(part_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
