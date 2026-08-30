from abc import ABC, abstractmethod

from src.ports.driver.for_manage_quotes.dto.quote_dto import QuoteDecisionDTO, QuoteDTO
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import ServiceOrderDTO


class ForManageQuote(ABC):
    @abstractmethod
    def read_quote(self, order_id: int) -> QuoteDTO:
        pass

    @abstractmethod
    def decide_quote(self, order_id: int, decision: QuoteDecisionDTO) -> ServiceOrderDTO:
        pass
