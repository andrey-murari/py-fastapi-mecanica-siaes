from abc import ABC, abstractmethod

from src.ports.driver.for_authenticate.dto import AdminIdentityDTO, LoginDTO, TokenDTO


class ForAuthenticate(ABC):
    @abstractmethod
    def login(self, credentials: LoginDTO) -> TokenDTO:
        pass

    @abstractmethod
    def current_admin(self, token: str) -> AdminIdentityDTO:
        pass
