from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.schemas.schemas import ReservationCreate, ReservationOut, ReservationUpdate
from app.models.models import Reservation, ReservationStatus, GuestDetails, PaymentEntry
from app.services.services import create_reservation, get_reservation, update_reservation, list_reservations
import json

router = APIRouter()

def calculate_amount(price_per_day: float, check_in_date, check_out_date):
    days = (check_out_date - check_in_date).days
    base = price_per_day * days
    tax = base * 0.02
    service_charge = base * 0.01
    total = base + tax + service_charge
    return base, tax, service_charge, total

@router.post("/reservations", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
def create_reservation_api(reservation_in: ReservationCreate):
    base, tax, service_charge, total = calculate_amount(
        reservation_in.price_per_day, reservation_in.check_in_date, reservation_in.check_out_date
    )
    guest_details = reservation_in.guest_details.model_dump()
    payments = [p.model_dump() for p in reservation_in.payments]
    reservation = Reservation(
        guest_details=json.dumps(guest_details),
        check_in_date=reservation_in.check_in_date,
        check_out_date=reservation_in.check_out_date,
        room_id=str(reservation_in.room_id),
        price_per_day=reservation_in.price_per_day,
        tax=tax,
        service_charge=service_charge,
        total_amount=total,
        payments=json.dumps(payments),
    )
    try:
        created = create_reservation(reservation)
        # Prepare output
        created_dict = created.model_dump()
        created_dict["guest_details"] = guest_details
        created_dict["payments"] = payments
        return created_dict
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reservations/{reservation_id}", response_model=ReservationOut)
def get_reservation_api(reservation_id: UUID):
    reservation = get_reservation(str(reservation_id))
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    res_dict = reservation.model_dump()
    res_dict["guest_details"] = json.loads(reservation.guest_details)
    res_dict["payments"] = json.loads(reservation.payments)
    return res_dict

@router.put("/reservations/{reservation_id}", response_model=ReservationOut)
def update_reservation_api(reservation_id: UUID, update: ReservationUpdate):
    payments = None
    if update.payments is not None:
        payments = json.dumps([p.model_dump() for p in update.payments])
    try:
        updated = update_reservation(str(reservation_id), update.status, payments)
        updated_dict = updated.model_dump()
        updated_dict["guest_details"] = json.loads(updated.guest_details)
        updated_dict["payments"] = json.loads(updated.payments)
        return updated_dict
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reservations", response_model=List[ReservationOut])
def list_reservations_api(status: Optional[ReservationStatus] = None):
    reservations = list_reservations(status)
    result = []
    for reservation in reservations:
        res_dict = reservation.model_dump()
        res_dict["guest_details"] = json.loads(reservation.guest_details)
        res_dict["payments"] = json.loads(reservation.payments)
        result.append(res_dict)
    return result
