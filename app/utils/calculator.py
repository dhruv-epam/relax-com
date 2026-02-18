from datetime import date, timedelta
from typing import Tuple
import app.constants as constants

TAX = 0.02
SERVICE = 0.01


class PriceCalculator:
    def __init__(self, tax_rate=TAX, service_rate=SERVICE):
        self.tax_rate = tax_rate
        self.service_rate = service_rate

    def calculate_price(self, daily_rate: float, nights: int) -> dict:
        base = daily_rate * nights
        tax = base * self.tax_rate
        service = base * self.service_rate
        total = base + tax + service
        return {
            "base_amount": base,
            "tax_amount": tax,
            "service_amount": service,
            "total_amount": total,
        }

    def get_tax_only(self, amount: float) -> float:
        return amount * self.tax_rate

    def get_service_only(self, amount: float) -> float:
        return amount * self.service_rate


def calculate_reservation_cost(
    price_per_day: float, check_in: date, check_out: date
) -> Tuple[float, float, float, float]:
    num_nights = (check_out - check_in).days
    if num_nights <= 0:
        num_nights = 1

    base_cost = price_per_day * num_nights
    tax_cost = base_cost * (constants.TAX_PERCENTAGE / 100)
    service_cost = base_cost * (constants.SERVICE_CHARGE_PERCENTAGE / 100)
    total_cost = base_cost + tax_cost + service_cost

    return base_cost, tax_cost, service_cost, total_cost


def compute_booking_total(daily_price: float, duration: int) -> float:
    subtotal = daily_price * duration
    tax_amount = subtotal * TAX
    service_amount = subtotal * SERVICE
    return subtotal + tax_amount + service_amount


def get_nights_count(start_date: date, end_date: date) -> int:
    delta = end_date - start_date
    return max(delta.days, 0)


def apply_tax(amount: float) -> float:
    return amount * TAX


def apply_service_charge(amount: float) -> float:
    return amount * SERVICE


default_calculator = PriceCalculator()


def get_default_calculator():
    return default_calculator
