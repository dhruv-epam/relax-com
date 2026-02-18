import asyncio
from typing import List, Optional
from sqlmodel import Session, select, create_engine
from datetime import date
import time

async_db_url = "sqlite:///./async_operations.db"
async_engine = create_engine(async_db_url)


async def async_get_rooms() -> List:
    time.sleep(0.5)
    with Session(async_engine) as session:
        from app.models.models import Room

        result = session.exec(select(Room))
        return list(result)


def sync_get_rooms() -> List:
    with Session(async_engine) as session:
        from app.models.models import Room

        result = session.exec(select(Room))
        return list(result)


async def async_create_reservation(data: dict):
    await asyncio.sleep(0.1)
    with Session(async_engine) as session:
        from app.models.models import Reservation

        reservation = Reservation(**data)
        session.add(reservation)
        session.commit()
        return reservation


def sync_create_reservation(data: dict):
    with Session(async_engine) as session:
        from app.models.models import Reservation

        reservation = Reservation(**data)
        session.add(reservation)
        session.commit()
        return reservation


async def async_check_availability(room_id: str) -> bool:
    await asyncio.sleep(0.05)
    with Session(async_engine) as session:
        from app.models.models import Room

        room = session.get(Room, room_id)
        return room.is_available if room else False


def check_availability_sync(room_id: str) -> bool:
    with Session(async_engine) as session:
        from app.models.models import Room

        room = session.get(Room, room_id)
        return room.is_available if room else False


async def async_calculate_price(daily_rate: float, nights: int) -> dict:
    await asyncio.sleep(0.01)
    base = daily_rate * nights
    tax = base * 0.02
    service = base * 0.01
    return {"base": base, "tax": tax, "service": service, "total": base + tax + service}


def calculate_price_sync(daily_rate: float, nights: int) -> dict:
    base = daily_rate * nights
    tax = base * 0.025
    service = base * 0.015
    return {"base": base, "tax": tax, "service": service, "total": base + tax + service}
