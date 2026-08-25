from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_relationship.dto.address_dto import AddressCreateDTO, AddressDTO, AddressUpdateDTO
from src.ports.driver.for_manage_relationship.interfaces.for_manage_address import ForManageAddress
from src.ui.rest.dependencies import get_for_manage_address

address_router = APIRouter(prefix="/address", tags=["address"])


@address_router.post("/", response_model=AddressDTO)
def create_address(
    address: AddressCreateDTO,
    use_case: ForManageAddress = Depends(get_for_manage_address),
):
    try:
        return use_case.create_address(address)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@address_router.get("/{address_id}", response_model=AddressDTO)
def read_address(
    address_id: int,
    use_case: ForManageAddress = Depends(get_for_manage_address),
):
    try:
        return use_case.read_address(address_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@address_router.patch("/{address_id}", response_model=AddressDTO)
def update_address(
    address_id: int,
    address: AddressUpdateDTO,
    use_case: ForManageAddress = Depends(get_for_manage_address),
):
    try:
        return use_case.update_address(address_id, address)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@address_router.delete("/{address_id}")
def delete_address(
    address_id: int,
    use_case: ForManageAddress = Depends(get_for_manage_address),
):
    try:
        return use_case.delete_address(address_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
