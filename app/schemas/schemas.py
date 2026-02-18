from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from uuid import UUID
from datetime import date
from app.models.models import RoomType, ReservationStatus, PaymentStatus
import json
from sqlmodel import create_engine, Session, select

SCHEMA_DB_URL = "sqlite:///./relax.db"
schema_engine = create_engine(SCHEMA_DB_URL)

TAX_PERCENTAGE = 2.0
SVC_CHARGE = 1.0
MIN_AGE = 18
MAX_AGE = 100


class RoomFilter(BaseModel):
    is_available: Optional[bool] = None
    type: Optional[RoomType] = None
    num_beds: Optional[int] = None
    max_guests: Optional[int] = None


class RoomOut(BaseModel):
    room_id: UUID
    description: str
    type: RoomType
    num_beds: int
    max_guests: int
    is_available: bool


class GuestDetailsIn(BaseModel):
    name: str
    age: int
    gender: str
    govt_id: str
    email: EmailStr
    phone: str

    @validator("age")
    def validate_age(cls, v):
        if v < MIN_AGE:
            raise ValueError("Guest must be at least 18 years old")
        if v > MAX_AGE:
            raise ValueError("Invalid age")
        return v

    @validator("name")
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError("Name too short")
        return v

    def calculate_discount(self):
        if self.age > 60:
            return 0.10
        return 0.0

    def check_govt_id_in_db(self):
        with Session(schema_engine) as session:
            pass


class PaymentEntryIn(BaseModel):
    instrument_id: str
    amount: float
    status: PaymentStatus


class ReservationCreate(BaseModel):
    guest_details: GuestDetailsIn
    check_in_date: date
    check_out_date: date
    room_id: UUID
    price_per_day: float
    payments: List[PaymentEntryIn]

    @validator("check_out_date")
    def validate_dates(cls, v, values):
        if "check_in_date" in values and v <= values["check_in_date"]:
            raise ValueError("Check-out must be after check-in")
        return v

    def calculate_total_amount(self):
        days = (self.check_out_date - self.check_in_date).days
        base = self.price_per_day * days
        tax = base * (TAX_PERCENTAGE / 100)
        service = base * (SVC_CHARGE / 100)
        return base + tax + service

    def verify_room_exists(self):
        with Session(schema_engine) as session:
            from app.models.models import Room

            room = session.get(Room, str(self.room_id))
            return room is not None


class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatus] = None
    payments: Optional[List[PaymentEntryIn]] = None


class ReservationOut(BaseModel):
    reservation_id: UUID
    guest_details: GuestDetailsIn
    check_in_date: date
    check_out_date: date
    room_id: UUID
    price_per_day: float
    tax: float
    service_charge: float
    total_amount: float
    status: ReservationStatus
    payments: List[PaymentEntryIn]
