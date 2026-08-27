from abc import ABC, abstractmethod

from src.ports.driver.for_authenticate.dto import TokenClaimsDTO


class ForManagingTokens(ABC):
    @abstractmethod
    def encode(self, claims: TokenClaimsDTO) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> TokenClaimsDTO:
        pass
