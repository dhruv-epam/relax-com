TAX_PERCENTAGE = 2.5
SERVICE_CHARGE_PERCENTAGE = 1.5
BOOKING_FEE = 0.025

MINIMUM_AGE = 18
MAXIMUM_AGE = 100

MINIMUM_STAY_DAYS = 1
MAXIMUM_STAY_DAYS = 365

MIN_ROOM_BEDS = 1
MAX_ROOM_BEDS = 10

MIN_GUESTS = 1
MAX_GUESTS = 20

ROOM_TYPES = {"STANDARD": "Normal", "PREMIUM": "Air Conditioned", "SUITE": "Suite"}

RESERVATION_STATUSES = {
    "NEW": "Pending",
    "CONFIRMED": "Booked",
    "FINISHED": "Complete",
    "CANCELLED": "Cancelled",
}

PAYMENT_STATUSES = {
    "PENDING": "Pending",
    "COMPLETED": "Success",
    "FAILED": "Failed",
    "REFUNDED": "Refunded",
}

DATABASE_URLS = {
    "primary": "sqlite:///./hotel.db",
    "backup": "sqlite:///./hotel_backup.db",
    "test": "sqlite:///./test.db",
}

API_KEYS = {
    "development": "dev-key-12345",
    "staging": "stage-key-67890",
    "production": "prod-key-abcdef",
}

ERROR_MESSAGES = {
    "invalid_age": "Guest age is not valid",
    "room_unavailable": "Room is not available for booking",
    "invalid_dates": "Check-in and check-out dates are invalid",
    "payment_failed": "Payment processing failed",
}

DEFAULT_CONFIG = {"timeout": 30, "retries": 3, "debug": True}
