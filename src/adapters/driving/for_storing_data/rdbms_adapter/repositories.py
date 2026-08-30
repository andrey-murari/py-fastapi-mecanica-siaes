from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

_PERSON_ID_FK = "person.person_id"


class Base(DeclarativeBase):
    ...


class UserRepository(Base):
    __tablename__ = "user"

    user_id: Mapped[str] = mapped_column(String(14), primary_key=True)
    user_type: Mapped[str] = mapped_column(String(20))
    login: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PersonRepository(Base):
    __tablename__ = "person"

    person_id: Mapped[str] = mapped_column(String(14), primary_key=True)
    complete_name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[str | None] = mapped_column(String(14), unique=True, nullable=True)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_customer: Mapped[bool] = mapped_column(Boolean)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class AddressRepository(Base):
    __tablename__ = "address"

    cep_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    street: Mapped[str] = mapped_column(String(255))
    neighborhood: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(2))
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class PersonAddressRepository(Base):
    __tablename__ = "person_address"

    person_address_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[str] = mapped_column(String(14), ForeignKey(_PERSON_ID_FK))
    cep_id: Mapped[str] = mapped_column(String(8), ForeignKey("address.cep_id"))
    number: Mapped[str] = mapped_column(String(20))
    complement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PersonContactRepository(Base):
    __tablename__ = "person_contact"

    contact_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[str] = mapped_column(String(14), ForeignKey(_PERSON_ID_FK))
    contact_type: Mapped[str] = mapped_column(String(20))
    value: Mapped[str] = mapped_column(String(255))
    flag_preferred: Mapped[bool] = mapped_column(Boolean)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class VehicleRepository(Base):
    __tablename__ = "vehicle"

    vehicle_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[str] = mapped_column(String(14), ForeignKey(_PERSON_ID_FK))
    model: Mapped[str] = mapped_column(String(100))
    brand: Mapped[str] = mapped_column(String(50))
    manufacture_year: Mapped[str] = mapped_column(String(4))
    model_year: Mapped[str] = mapped_column(String(4))
    engine: Mapped[str] = mapped_column(String(50))
    fuel_type: Mapped[str] = mapped_column(String(20))
    plate: Mapped[str] = mapped_column(String(7), unique=True)
    color: Mapped[str] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ServiceRepository(Base):
    __tablename__ = "service"

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    average_duration_minutes: Mapped[int] = mapped_column(Integer)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PartRepository(Base):
    __tablename__ = "part"

    part_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255))
    brand: Mapped[str] = mapped_column(String(100))
    manufacturer: Mapped[str] = mapped_column(String(100))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    available_quantity: Mapped[int] = mapped_column(Integer)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ServiceOrderRepository(Base):
    __tablename__ = "service_order"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[str] = mapped_column(String(14), ForeignKey(_PERSON_ID_FK))
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey("vehicle.vehicle_id"))
    mileage: Mapped[int] = mapped_column(Integer)
    reported_problem: Mapped[str] = mapped_column(String(2000))
    diagnosis: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    mechanic_id: Mapped[str | None] = mapped_column(
        String(14), ForeignKey("user.user_id"), nullable=True
    )
    services_total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    parts_total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estimated_duration_days: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(80))
    request_date: Mapped[datetime] = mapped_column(DateTime)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class OrderServiceRepository(Base):
    __tablename__ = "order_service"

    order_service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_order.order_id"))
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey("service.service_id"))
    mechanic_id: Mapped[str | None] = mapped_column(
        String(14), ForeignKey("user.user_id"), nullable=True
    )
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class OrderPartRepository(Base):
    __tablename__ = "order_part"

    order_part_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_order.order_id"))
    part_id: Mapped[int] = mapped_column(Integer, ForeignKey("part.part_id"))
    quantity: Mapped[int] = mapped_column(Integer)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    user_modification_id: Mapped[int] = mapped_column(Integer)
    flag_active: Mapped[bool] = mapped_column(Boolean)
    insertion_date: Mapped[datetime] = mapped_column(DateTime)
    modification_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class StockOperationRepository(Base):
    __tablename__ = "stock_operation"

    operation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    part_id: Mapped[int] = mapped_column(Integer, ForeignKey("part.part_id"))
    operation_type: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(Integer)
    order_part_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("order_part.order_part_id"), unique=True, nullable=True
    )
    operation_date: Mapped[datetime] = mapped_column(DateTime)
