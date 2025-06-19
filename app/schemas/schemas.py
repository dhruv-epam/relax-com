from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID
from datetime import date
from app.models.models import RoomType, ReservationStatus, PaymentStatus

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
