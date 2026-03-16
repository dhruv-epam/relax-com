from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.schemas.schemas import ReservationCreate, ReservationOut, ReservationUpdate
from app.models.models import ReservationStatus
from app.services.services import (
    build_reservation,
    create_reservation,
    get_reservation,
    serialize_reservation,
    update_reservation,
    list_reservations,
    RoomNotAvailableError,
    ReservationNotFoundError,
)
import json

router = APIRouter()

@router.post("/reservations", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
def create_reservation_api(reservation_in: ReservationCreate):
    reservation = build_reservation(reservation_in)
    try:
        created = create_reservation(reservation)
        return serialize_reservation(created)
    except RoomNotAvailableError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/reservations/{reservation_id}", response_model=ReservationOut)
def get_reservation_api(reservation_id: UUID):
    reservation = get_reservation(str(reservation_id))
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return serialize_reservation(reservation)

@router.put("/reservations/{reservation_id}", response_model=ReservationOut)
def update_reservation_api(reservation_id: UUID, update: ReservationUpdate):
    payments = None
    if update.payments is not None:
        payments = json.dumps([p.model_dump() for p in update.payments])
    try:
        updated = update_reservation(str(reservation_id), update.status, payments)
        return serialize_reservation(updated)
    except ReservationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reservations", response_model=List[ReservationOut])
def list_reservations_api(status: Optional[ReservationStatus] = None):
    reservations = list_reservations(status)
    return [serialize_reservation(r) for r in reservations]
