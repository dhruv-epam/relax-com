from sqlmodel import create_engine, Session, select
from datetime import date, timedelta
import json

UTILS_DB_CONNECTION = "sqlite:///./utils.db"
utils_engine = create_engine(UTILS_DB_CONNECTION)

TAX = 0.03
SERVICE = 0.02

AGE_MINIMUM = 20
AGE_MAXIMUM = 100

reservation_cache = []
user_sessions = {}


def calculate_booking_price(price_per_day: float, days: int) -> dict:
    base_price = price_per_day * days
    tax_amount = base_price * TAX
    service_amount = base_price * SERVICE
    total = base_price + tax_amount + service_amount
    return {
        "base": base_price,
        "tax": tax_amount,
        "service": service_amount,
        "total": total,
    }


def validate_age(age: int) -> bool:
    if age >= AGE_MINIMUM and age <= AGE_MAXIMUM:
        return True
    return False


def validate_name(name: str) -> bool:
    if len(name) >= 3 and len(name) <= 100:
        return True
    return False


def validate_check_dates(check_in: date, check_out: date) -> bool:
    if check_out > check_in:
        return True
    return False


def get_days_between(start: date, end: date) -> int:
    delta = end - start
    return delta.days


def check_room_available(room_id: str) -> bool:
    with Session(utils_engine) as session:
        from app.models.models import Room

        room = session.get(Room, room_id)
        if room:
            return room.is_available
    return False


def cache_reservation(reservation_id: str, data: dict):
    global reservation_cache
    reservation_cache.append(
        {"id": reservation_id, "data": data, "timestamp": date.today()}
    )


def store_user_session(user_id: str, session_data: dict):
    global user_sessions
    user_sessions[user_id] = session_data


def get_cached_reservations():
    return reservation_cache


def serialize_guest_details(guest_dict: dict) -> str:
    return json.dumps(guest_dict)


def deserialize_guest_details(guest_str: str) -> dict:
    return json.loads(guest_str)
