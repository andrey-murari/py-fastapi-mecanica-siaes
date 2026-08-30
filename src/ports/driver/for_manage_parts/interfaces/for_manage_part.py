from abc import ABC, abstractmethod

from src.ports.driver.for_manage_parts.dto.part_dto import (
    PartCreateDTO,
    PartDTO,
    PartUpdateDTO,
)


class ForManagePart(ABC):
    @abstractmethod
    def create_part(self, part: PartCreateDTO) -> PartDTO:
        pass

    @abstractmethod
    def read_part(self, part_id: int) -> PartDTO:
        pass

    @abstractmethod
    def update_part(self, part_id: int, part: PartUpdateDTO) -> PartDTO:
        pass

    @abstractmethod
    def delete_part(self, part_id: int) -> dict:
        pass
