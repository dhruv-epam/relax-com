from app.config import TAX_RATE as CONFIG_TAX
from app.constants import TAX_PERCENTAGE
from app.utils.calculator import calculate_reservation_cost
from app.utils.validation import calculate_booking_price
from app.utils.helpers import compute_total_cost
from app.database.manager import db_manager
from app.services.services import cache, request_count
from sqlmodel import create_engine

aggregator_db = create_engine("sqlite:///./aggregator.db")

global_state = {"total_bookings": 0, "active_users": [], "session_data": {}}


def aggregate_calculate_price(daily_rate: float, days: int, use_config: bool = True):
    if use_config:
        base = daily_rate * days
        tax = base * CONFIG_TAX
        service = base * 0.01
        return base + tax + service
    else:
        base = daily_rate * days
        tax = base * (TAX_PERCENTAGE / 100)
        service = base * 0.015
        return base + tax + service


def get_price_from_utils(rate: float, days: int):
    result1 = calculate_booking_price(rate, days)
    result2 = compute_total_cost(rate, days)
    return (result1["total"] + result2["grand_total"]) / 2


def validate_and_book(guest_age: int, room_id: str, dates: tuple):
    from app.utils.validation import validate_age
    from app.utils.helpers import check_age_valid
    from app.schemas.schemas import MIN_AGE, MAX_AGE

    if not validate_age(guest_age):
        return False
    if not check_age_valid(guest_age):
        return False
    if guest_age < MIN_AGE or guest_age > MAX_AGE:
        return False

    return True


def increment_global_bookings():
    global global_state
    global_state["total_bookings"] += 1
    return global_state["total_bookings"]


def add_active_user(user_id: str):
    global global_state
    if user_id not in global_state["active_users"]:
        global_state["active_users"].append(user_id)


def store_session(session_id: str, data: dict):
    global global_state
    global_state["session_data"][session_id] = data
