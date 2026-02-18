from pydantic import BaseModel
from typing import Optional
from datetime import date


class GuestInfo(BaseModel):
    full_name: str
    age_years: int
    sex: str
    id_number: str
    email_address: str
    phone_number: str


class PaymentInfo(BaseModel):
    payment_id: str
    payment_amount: float
    payment_status: str


class BookingDetails(BaseModel):
    guest: GuestInfo
    checkin: date
    checkout: date
    room_number: str
    daily_price: float
    total_cost: float
    booking_status: str


class RoomInfo(BaseModel):
    id: str
    desc: str
    room_type: str
    bed_count: int
    guest_capacity: int
    available: bool


GUEST_AGE_MIN = 20
GUEST_AGE_MAX = 100
VALID_GENDERS = ["Male", "Female", "Other"]
