from fastapi import APIRouter, Depends, HTTPException

from src.ports.driver.for_manage_quotes.dto.quote_dto import QuoteDecisionDTO, QuoteDTO
from src.ports.driver.for_manage_quotes.interfaces.for_manage_quote import ForManageQuote
from src.ports.driver.for_manage_service_orders.dto.service_order_dto import ServiceOrderDTO
from src.ui.rest.dependencies import get_for_manage_quote

quote_router = APIRouter(prefix="/quote", tags=["quote"])


def _http_from(exc: ValueError) -> HTTPException:
    status_code = 404 if str(exc) in {"Order not found", "Vehicle not found"} else 400
    return HTTPException(status_code=status_code, detail=str(exc))


@quote_router.get("/{order_id}", response_model=QuoteDTO)
def read_quote(
    order_id: int,
    use_case: ForManageQuote = Depends(get_for_manage_quote),
):
    try:
        return use_case.read_quote(order_id)
    except ValueError as exc:
        raise _http_from(exc) from exc


@quote_router.patch("/{order_id}", response_model=ServiceOrderDTO)
def decide_quote(
    order_id: int,
    decision: QuoteDecisionDTO,
    use_case: ForManageQuote = Depends(get_for_manage_quote),
):
    try:
        return use_case.decide_quote(order_id, decision)
    except ValueError as exc:
        raise _http_from(exc) from exc
