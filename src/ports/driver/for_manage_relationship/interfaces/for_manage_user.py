from abc import ABC, abstractmethod

from src.ports.driver.for_manage_relationship.dto.user_dto import UserCreateDTO, UserDTO


class ForManageUser(ABC):
    @abstractmethod
    def create_user(self, user: UserCreateDTO) -> UserDTO:
        pass
