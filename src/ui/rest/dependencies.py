from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.ports.driver.for_authenticate.dto import AdminIdentityDTO
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ports.driver.for_manage_relationship.interfaces.for_manage_user import ForManageUser
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ports.driver.for_manage_parts.interfaces.for_manage_part import ForManagePart
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import (
    ForManageInventory,
)
from src.ports.driver.for_manage_quotes.interfaces.for_manage_quote import ForManageQuote
from src.ports.driver.for_manage_service_orders.interfaces.for_manage_service_order import ForManageServiceOrder
from src.ports.driver.for_manage_services.interfaces.for_manage_service import ForManageService

_for_manage_customer: ForManageCustomer | None = None
_for_manage_person: ForManagePerson | None = None
_for_manage_user: ForManageUser | None = None
_for_manage_vehicle: ForManageVehicle | None = None
_for_manage_service: ForManageService | None = None
_for_manage_part: ForManagePart | None = None
_for_manage_inventory: ForManageInventory | None = None
_for_manage_service_order: ForManageServiceOrder | None = None
_for_manage_quote: ForManageQuote | None = None
_for_authenticate: ForAuthenticate | None = None
_bearer = HTTPBearer(auto_error=False)


def set_for_manage_customer(port: ForManageCustomer) -> None:
    global _for_manage_customer
    _for_manage_customer = port


def get_for_manage_customer() -> ForManageCustomer:
    if _for_manage_customer is None:
        raise RuntimeError("ForManageCustomer was not wired in main.py")
    return _for_manage_customer


def set_for_manage_person(port: ForManagePerson) -> None:
    global _for_manage_person
    _for_manage_person = port


def get_for_manage_person() -> ForManagePerson:
    if _for_manage_person is None:
        raise RuntimeError("ForManagePerson was not wired in main.py")
    return _for_manage_person


def set_for_manage_user(port: ForManageUser) -> None:
    global _for_manage_user
    _for_manage_user = port


def get_for_manage_user() -> ForManageUser:
    if _for_manage_user is None:
        raise RuntimeError("ForManageUser was not wired in main.py")
    return _for_manage_user


def set_for_manage_vehicle(port: ForManageVehicle) -> None:
    global _for_manage_vehicle
    _for_manage_vehicle = port


def get_for_manage_vehicle() -> ForManageVehicle:
    if _for_manage_vehicle is None:
        raise RuntimeError("ForManageVehicle was not wired in main.py")
    return _for_manage_vehicle


def set_for_manage_service(port: ForManageService) -> None:
    global _for_manage_service
    _for_manage_service = port


def get_for_manage_service() -> ForManageService:
    if _for_manage_service is None:
        raise RuntimeError("ForManageService was not wired in main.py")
    return _for_manage_service


def set_for_manage_part(port: ForManagePart) -> None:
    global _for_manage_part
    _for_manage_part = port


def get_for_manage_part() -> ForManagePart:
    if _for_manage_part is None:
        raise RuntimeError("ForManagePart was not wired in main.py")
    return _for_manage_part


def set_for_manage_inventory(port: ForManageInventory) -> None:
    global _for_manage_inventory
    _for_manage_inventory = port


def get_for_manage_inventory() -> ForManageInventory:
    if _for_manage_inventory is None:
        raise RuntimeError("ForManageInventory was not wired in main.py")
    return _for_manage_inventory


def set_for_manage_service_order(port: ForManageServiceOrder) -> None:
    global _for_manage_service_order
    _for_manage_service_order = port


def get_for_manage_service_order() -> ForManageServiceOrder:
    if _for_manage_service_order is None:
        raise RuntimeError("ForManageServiceOrder was not wired in main.py")
    return _for_manage_service_order


def set_for_manage_quote(port: ForManageQuote) -> None:
    global _for_manage_quote
    _for_manage_quote = port


def get_for_manage_quote() -> ForManageQuote:
    if _for_manage_quote is None:
        raise RuntimeError("ForManageQuote was not wired in main.py")
    return _for_manage_quote


def set_for_authenticate(port: ForAuthenticate) -> None:
    global _for_authenticate
    _for_authenticate = port


def get_for_authenticate() -> ForAuthenticate:
    if _for_authenticate is None:
        raise RuntimeError("ForAuthenticate was not wired in main.py")
    return _for_authenticate


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    auth: ForAuthenticate = Depends(get_for_authenticate),
) -> AdminIdentityDTO:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return auth.current_admin(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
