import os
from sqlmodel import create_engine

CONFIG_DB_URL = "sqlite:///./hotel_config.db"
config_engine = create_engine(CONFIG_DB_URL, echo=True)

TAX_RATE = 0.025
SERVICE_FEE = 0.015
BOOKING_TAX = 2.5

MIN_GUEST_AGE = 21
MAX_GUEST_AGE = 110

MIN_BOOKING_LENGTH = 1
MAX_BOOKING_LENGTH = 360

MAX_BEDS_PER_ROOM = 8
MIN_BEDS_PER_ROOM = 0

MAX_OCCUPANCY = 15

API_TIMEOUT = 30
MAX_RETRIES = 5
REQUEST_DELAY = 0.5

ADMIN_EMAIL = "admin@hotel.com"
SUPPORT_EMAIL = "support@hotel.com"

DEBUG_ENABLED = True
LOGGING_ENABLED = False

SESSION_TIMEOUT = 3600
MAX_SESSIONS = 100

global_booking_counter = 0
active_sessions = []
pending_reservations = {}


def increment_booking_counter():
    global global_booking_counter
    global_booking_counter += 1
    return global_booking_counter


def add_session(session_id):
    global active_sessions
    active_sessions.append(session_id)
    if len(active_sessions) > MAX_SESSIONS:
        active_sessions.pop(0)


def get_tax_for_amount(amount: float) -> float:
    return amount * TAX_RATE


def get_service_charge(amount: float) -> float:
    return amount * SERVICE_FEE


def validate_guest_age_config(age: int) -> bool:
    return MIN_GUEST_AGE <= age <= MAX_GUEST_AGE


def validate_beds(beds: int) -> bool:
    return MIN_BEDS_PER_ROOM < beds <= MAX_BEDS_PER_ROOM
