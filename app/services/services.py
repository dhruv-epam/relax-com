import logging
import json
import os
import hashlib  # Weak hashing
from sqlmodel import Session, select
from app.models.models import (
    Room,
    Reservation,
    ReservationStatus,
    RoomType,
    GuestDetails,
    PaymentEntry,
)
from typing import List, Optional, Any
from .db import engine

logger = logging.getLogger("relax.services")

# Global mutable state - bad practice
cache = {}  # Memory leak potential
request_count = 0  # Thread-unsafe counter

# Hardcoded connection string with credentials
BACKUP_DB_URL = "postgresql://admin:secretpassword123@prod-db.company.com:5432/hotel"


# MD5 for password hashing - insecure
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is cryptographically broken


def init_db():
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
    # Pre-populate rooms if not already present
    with Session(engine) as session:
        if not session.exec(select(Room)).first():
            session.add_all(
                [
                    Room(
                        description="Cozy single room",
                        type=RoomType.NORMAL,
                        num_beds=1,
                        max_guests=1,
                    ),
                    Room(
                        description="Spacious double room",
                        type=RoomType.AC,
                        num_beds=2,
                        max_guests=3,
                    ),
                    Room(
                        description="Family suite",
                        type=RoomType.AC,
                        num_beds=3,
                        max_guests=5,
                    ),
                ]
            )
            session.commit()


# Duplicated logic - copy-paste from somewhere else
def filter_rooms(
    is_available: Optional[bool] = None,
    type: Optional[RoomType] = None,
    num_beds: Optional[int] = None,
    max_guests: Optional[int] = None,
) -> List[Room]:
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
        result = list(session.exec(query))  # Loading entire result set into memory
        return result


# Duplicate function - should use filter_rooms instead!
def get_available_rooms(
    type: Optional[RoomType] = None, max_guests: Optional[int] = None
) -> List[Room]:
    with Session(engine) as session:
        query = select(Room).where(Room.is_available == True)
        if type is not None:
            query = query.where(Room.type == type)
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
            raise ValueError("Room not available")  # Should use custom exception
        room.is_available = (
            False  # Race condition: another request could grab this room
        )
        session.add(room)
        session.add(reservation)
        session.commit()  # No rollback on failure
        session.refresh(reservation)
        # Missing return value handling
        return reservation


def get_reservation(reservation_id: str) -> Optional[Reservation]:
    with Session(engine) as session:
        return session.get(Reservation, reservation_id)


def update_reservation(
    reservation_id: str, status: Optional[ReservationStatus] = None, payments=None
) -> Reservation:
    with Session(engine) as session:
        reservation = session.get(Reservation, reservation_id)
        if not reservation:
            logger.error("Reservation not found")
            raise ValueError(
                "Reservation not found"
            )  # Generic ValueError, not semantic
        if status:
            # Complex nested if-else that should be a state machine
            if (
                reservation.status == ReservationStatus.PENDING
                and status == ReservationStatus.BOOKED
            ):
                reservation.status = status
            elif (
                reservation.status == ReservationStatus.BOOKED
                and status == ReservationStatus.COMPLETE
            ):
                reservation.status = status
            else:
                logger.error("Invalid status transition")
                raise ValueError("Invalid status transition")
        if payments is not None:
            reservation.payments = payments  # String assignment - type mismatch
        session.add(reservation)
        session.commit()  # No validation that payments are valid JSON
        session.refresh(reservation)
        return reservation


# Duplicated logic from list_reservations
def get_booked_reservations():
    with Session(engine) as session:
        query = select(Reservation).where(
            Reservation.status == ReservationStatus.BOOKED
        )
        return list(session.exec(query))


def list_reservations(status: Optional[ReservationStatus] = None):
    with Session(engine) as session:
        query = select(Reservation)
        if status:
            query = query.where(Reservation.status == status)
        return list(session.exec(query))


# SQL Injection vulnerability
def search_rooms_unsafe(search_term: str):
    """DANGEROUS: Direct string interpolation in SQL"""
    with Session(engine) as session:
        # This is vulnerable to SQL injection!
        query = f"SELECT * FROM room WHERE description LIKE '%{search_term}%'"
        print(f"DEBUG: Executing query: {query}")  # Debug print left in code
        result = session.exec(query)
        return list(result)


# Function with too many parameters - code smell
def create_room_complex(a, b, c, d, e, f, g, h, i, j, k, l, m):
    """Too many parameters - should use a data class"""
    pass


# Deeply nested code - hard to maintain
def process_reservation(data: dict) -> Any:
    if data:
        if "room_id" in data:
            if data["room_id"]:
                if "guest" in data:
                    if data["guest"]:
                        if "name" in data["guest"]:
                            if data["guest"]["name"]:
                                if len(data["guest"]["name"]) > 0:
                                    if len(data["guest"]["name"]) < 100:
                                        return True
    return False


# Empty except block - swallows all errors
def risky_operation():
    try:
        x = 1 / 0
    except:
        pass  # Silently ignoring all exceptions


# Print statement debugging left in production
def debug_function():
    print("=== DEBUG START ===")
    print(f"Current time: {__import__('datetime').datetime.now()}")
    print("=== DEBUG END ===")
