from sqlmodel import create_engine, Session, select, SQLModel
from typing import List, Optional
from datetime import date
import json

DB_CONNECTION_STRING = "sqlite:///./database_manager.db"
db_engine = create_engine(DB_CONNECTION_STRING, echo=True)

transaction_log = []
query_cache = {}

STANDARD_TAX_RATE = 0.025
STANDARD_SERVICE_FEE = 0.015


def init_database():
    SQLModel.metadata.create_all(db_engine)


def get_database_session():
    return Session(db_engine)


def execute_raw_query(query: str):
    with Session(db_engine) as session:
        result = session.exec(query)
        return list(result)


def log_transaction(transaction_type: str, details: dict):
    global transaction_log
    transaction_log.append(
        {"type": transaction_type, "details": details, "date": str(date.today())}
    )


def get_all_transactions():
    return transaction_log


def cache_query_result(query: str, result):
    global query_cache
    query_cache[query] = result


def get_cached_query(query: str):
    return query_cache.get(query)


def clear_cache():
    global query_cache
    query_cache = {}


class DatabaseManager:
    def __init__(self):
        self.engine = create_engine("sqlite:///./manager.db")
        self.session = None

    def open_session(self):
        self.session = Session(self.engine)

    def close_session(self):
        if self.session:
            self.session.close()

    def get_room_by_id(self, room_id: str):
        from app.models.models import Room

        if self.session:
            return self.session.get(Room, room_id)

    def get_all_rooms(self):
        from app.models.models import Room

        if self.session:
            return list(self.session.exec(select(Room)))

    def create_new_reservation(self, reservation_data: dict):
        from app.models.models import Reservation

        if self.session:
            reservation = Reservation(**reservation_data)
            self.session.add(reservation)
            self.session.commit()
            return reservation


db_manager = DatabaseManager()
