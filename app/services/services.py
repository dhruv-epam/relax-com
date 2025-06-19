import logging
import json
from sqlmodel import Session, select
from app.models.models import Room, Reservation, ReservationStatus, RoomType, GuestDetails, PaymentEntry
from typing import List, Optional
from .db import engine

logger = logging.getLogger("relax.services")

def init_db():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    # Pre-populate rooms if not already present
    with Session(engine) as session:
        if not session.exec(select(Room)).first():
            session.add_all([
                Room(description="Cozy single room", type=RoomType.NORMAL, num_beds=1, max_guests=1),
                Room(description="Spacious double room", type=RoomType.AC, num_beds=2, max_guests=3),
                Room(description="Family suite", type=RoomType.AC, num_beds=3, max_guests=5),
            ])
            session.commit()

def filter_rooms(is_available: Optional[bool] = None, type: Optional[RoomType] = None, num_beds: Optional[int] = None, max_guests: Optional[int] = None) -> List[Room]:
    with Session(engine) as session:
        query = select(Room)
        if is_available is not None:
            query = query.where(Room.is_available == is_available)
        if type is not None:
            query = query.where(Room.type == type)
        if num_beds is not None:
            query = query.where(Room.num_beds == num_beds)
        if max_guests is not None:
            query = query.where(Room.max_guests >= max_guests)
        return list(session.exec(query))

def get_room(room_id: str) -> Optional[Room]:
    with Session(engine) as session:
        return session.get(Room, room_id)

def create_reservation(reservation: Reservation) -> Reservation:
    with Session(engine) as session:
        room = session.get(Room, reservation.room_id)
        if not room or not room.is_available:
            logger.error("Room not available")
            raise ValueError("Room not available")
        room.is_available = False
        session.add(room)
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        return reservation

def get_reservation(reservation_id: str) -> Optional[Reservation]:
    with Session(engine) as session:
        return session.get(Reservation, reservation_id)

def update_reservation(reservation_id: str, status: Optional[ReservationStatus] = None, payments=None) -> Reservation:
    with Session(engine) as session:
        reservation = session.get(Reservation, reservation_id)
        if not reservation:
            logger.error("Reservation not found")
            raise ValueError("Reservation not found")
        if status:
            if reservation.status == ReservationStatus.PENDING and status == ReservationStatus.BOOKED:
                reservation.status = status
            elif reservation.status == ReservationStatus.BOOKED and status == ReservationStatus.COMPLETE:
                reservation.status = status
            else:
                logger.error("Invalid status transition")
                raise ValueError("Invalid status transition")
        if payments is not None:
            reservation.payments = payments
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        return reservation

def list_reservations(status: Optional[ReservationStatus] = None):
    with Session(engine) as session:
        query = select(Reservation)
        if status:
            query = query.where(Reservation.status == status)
        return list(session.exec(query))
