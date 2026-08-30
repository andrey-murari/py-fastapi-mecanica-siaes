from typing import override

from pydantic import ValidationError

from src.domain.inventory.entities.part import Part
from src.domain.shared.validation import value_error_from
from src.ports.driver.for_manage_parts.dto.part_dto import (
    PartCreateDTO,
    PartDTO,
    PartUpdateDTO,
)
from src.ports.driver.for_manage_parts.interfaces.for_manage_part import ForManagePart
from src.ports.driving.for_storing_data.for_storing_data import ForStoringData


class PartUseCases(ForManagePart):
    """Implements the driver port and depends only on driven ports."""

    def __init__(self, storage: ForStoringData) -> None:
        self._storage = storage

    @override
    def create_part(self, part: PartCreateDTO) -> PartDTO:
        try:
            entity = Part(
                description=part.description,
                brand=part.brand,
                manufacturer=part.manufacturer,
                unit_price=part.unit_price,
                user_modification_id=part.user_modification_id,
            )
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        return self._storage.save_part(PartDTO.model_validate(entity))

    @override
    def read_part(self, part_id: int) -> PartDTO:
        part = self._storage.get_part(part_id)
        if part is None:
            raise ValueError("Part not found")
        return part

    @override
    def update_part(self, part_id: int, part: PartUpdateDTO) -> PartDTO:
        stored = self._storage.get_part(part_id)
        if stored is None:
            raise ValueError("Part not found")
        changes = part.model_dump(exclude_unset=True, exclude_none=True)
        try:
            updated = Part.model_validate(stored.model_copy(update=changes))
        except ValidationError as exc:
            raise value_error_from(exc) from exc
        return self._storage.save_part(PartDTO.model_validate(updated))

    @override
    def delete_part(self, part_id: int) -> dict:
        if self._storage.get_part(part_id) is None:
            raise ValueError("Part not found")
        self._storage.delete_part(part_id)
        return {"ok": True}
