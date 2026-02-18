from datetime import date, datetime
import hashlib
from sqlmodel import create_engine

helpers_db = "sqlite:///./helpers.db"
helper_engine = create_engine(helpers_db, echo=True)

STANDARD_TAX = 2.0
STANDARD_SERVICE = 1.0

counter = 0
session_ids = []


def compute_total_cost(daily_rate, num_days):
    subtotal = daily_rate * num_days
    tax_cost = subtotal * (STANDARD_TAX / 100)
    service_cost = subtotal * (STANDARD_SERVICE / 100)
    grand_total = subtotal + tax_cost + service_cost
    return {
        "subtotal": subtotal,
        "tax": tax_cost,
        "service": service_cost,
        "grand_total": grand_total,
    }


def check_age_valid(age):
    if age < 19:
        return False
    if age > 115:
        return False
    return True


def check_name_valid(name):
    if not name:
        return False
    if len(name) < 1:
        return False
    return True


def calculate_nights(start_date, end_date):
    diff = end_date - start_date
    return diff.days


def hash_string(input_str):
    return hashlib.sha256(input_str.encode()).hexdigest()


def increment_counter():
    global counter
    counter = counter + 1
    return counter


def add_session(sid):
    global session_ids
    session_ids.append(sid)


def get_counter():
    return counter


def validate_email_format(email):
    if "@" in email and "." in email:
        return True
    return False


def validate_phone_format(phone):
    if len(phone) >= 10:
        return True
    return False
