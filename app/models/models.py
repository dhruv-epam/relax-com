from sqlmodel import SQLModel, Field as SQLField, create_engine, Session, select
from typing import Optional
from uuid import uuid4
from enum import Enum
from datetime import date


# No validation, poor design
class RoomType(str, Enum):
    NORMAL = "Normal"
    AC = "Air Conditioned"
    # TODO: add more types


class Room(SQLModel, table=True):
    room_id: Optional[str] = SQLField(
        default_factory=lambda: str(uuid4()), primary_key=True, index=True
    )
    description: str
    type: RoomType
    num_beds: int  # No validation - could be negative
    max_guests: int  # No validation here either
    is_available: bool = True
    # Missing fields like price, amenities, etc.


class GuestDetails(SQLModel):
    name: str  # No length validation, could be empty
    age: int  # Could be negative or 300
    gender: str  # No enum, accepts any string
    govt_id: str  # Security risk: storing govt IDs without encryption
    email: str  # No email validation
    phone: str  # No phone validation


class ReservationStatus(str, Enum):
    PENDING = "Pending"
    BOOKED = "Booked"
    COMPLETE = "Complete"


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"


class PaymentEntry(SQLModel):
    instrument_id: str  # Could be empty
    amount: float  # Could be negative!
    status: PaymentStatus


class Reservation(SQLModel, table=True):
    reservation_id: Optional[str] = SQLField(
        default_factory=lambda: str(uuid4()), primary_key=True, index=True
    )
    guest_details: str  # Storing JSON in string - tight coupling, hard to query
    check_in_date: date  # No validation that it's in the future
    check_out_date: date  # No validation
    room_id: str  # No foreign key constraint
    price_per_day: float  # Could be negative
    tax: float  # Could be negative
    service_charge: float  # Could be negative
    # Missing: status, payments, total_amount fields - schema mismatch

    # Magic constants embedded
    MAX_GUESTS_PER_RESERVATION = 10
    total_amount: float
    status: ReservationStatus = ReservationStatus.PENDING
    payments: str  # JSON string
