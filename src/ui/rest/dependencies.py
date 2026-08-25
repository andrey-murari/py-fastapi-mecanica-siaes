from src.ports.driver.for_manage_relationship.interfaces.for_manage_address import ForManageAddress
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle

_for_manage_customer: ForManageCustomer | None = None
_for_manage_address: ForManageAddress | None = None
_for_manage_person: ForManagePerson | None = None
_for_manage_vehicle: ForManageVehicle | None = None


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
