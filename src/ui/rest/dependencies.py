from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.ports.driver.for_authenticate.dto import AdminIdentityDTO
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ports.driver.for_manage_relationship.interfaces.for_manage_address import ForManageAddress
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle

_for_manage_customer: ForManageCustomer | None = None
_for_manage_address: ForManageAddress | None = None
_for_manage_person: ForManagePerson | None = None
_for_manage_vehicle: ForManageVehicle | None = None
_for_authenticate: ForAuthenticate | None = None
_bearer = HTTPBearer(auto_error=False)


def set_for_manage_customer(port: ForManageCustomer) -> None:
    global _for_manage_customer
    _for_manage_customer = port


def get_for_manage_customer() -> ForManageCustomer:
    if _for_manage_customer is None:
        raise RuntimeError("ForManageCustomer was not wired in main.py")
    return _for_manage_customer


def set_for_manage_address(port: ForManageAddress) -> None:
    global _for_manage_address
    _for_manage_address = port


def get_for_manage_address() -> ForManageAddress:
    if _for_manage_address is None:
        raise RuntimeError("ForManageAddress was not wired in main.py")
    return _for_manage_address


def set_for_manage_person(port: ForManagePerson) -> None:
    global _for_manage_person
    _for_manage_person = port


def get_for_manage_person() -> ForManagePerson:
    if _for_manage_person is None:
        raise RuntimeError("ForManagePerson was not wired in main.py")
    return _for_manage_person


def set_for_manage_vehicle(port: ForManageVehicle) -> None:
    global _for_manage_vehicle
    _for_manage_vehicle = port


def get_for_manage_vehicle() -> ForManageVehicle:
    if _for_manage_vehicle is None:
        raise RuntimeError("ForManageVehicle was not wired in main.py")
    return _for_manage_vehicle


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
