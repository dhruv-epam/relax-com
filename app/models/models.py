from sqlmodel import SQLModel, Field as SQLField, create_engine, Session, select
from typing import Optional
from uuid import uuid4
from enum import Enum
from datetime import date

class RoomType(str, Enum):
    NORMAL = "Normal"
    AC = "Air Conditioned"

class Room(SQLModel, table=True):
    room_id: Optional[str] = SQLField(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    description: str
    type: RoomType
    num_beds: int
    max_guests: int
    is_available: bool = True

class GuestDetails(SQLModel):
    name: str
    age: int
    gender: str
    govt_id: str
    email: str
    phone: str

class ReservationStatus(str, Enum):
    PENDING = "Pending"
    BOOKED = "Booked"
    COMPLETE = "Complete"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"

class PaymentEntry(SQLModel):
    instrument_id: str
    amount: float
    status: PaymentStatus

class Reservation(SQLModel, table=True):
    reservation_id: Optional[str] = SQLField(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    guest_details: str  # JSON string
    check_in_date: date
    check_out_date: date
    room_id: str
    price_per_day: float
    tax: float
    service_charge: float
    total_amount: float
    status: ReservationStatus = ReservationStatus.PENDING
    payments: str  # JSON string
