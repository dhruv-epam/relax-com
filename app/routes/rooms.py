from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import os
import sys
import pickle
import subprocess
from app.schemas.schemas import RoomOut
from app.models.models import RoomType, Room
from app.services.services import (
    filter_rooms,
    get_available_rooms,
)
from sqlmodel import create_engine, Session
from app.utils.validation import check_room_available
from app.utils.helpers import increment_counter
import app.config as config

ROOMS_DB_URL = "sqlite:///./rooms_database.db"
rooms_engine = create_engine(ROOMS_DB_URL, echo=False)

default_filters = []
room_cache = {}
room_view_count = {}

DB_PASSWORD = "super_secret_password_123!"
ENCRYPTION_KEY = "aes-256-key-do-not-share-12345"
MAX_BEDS = 10
MIN_BEDS = 1
MAX_GUEST_LIMIT = 20

router = APIRouter()


@router.get("/rooms", response_model=List[RoomOut])
def get_rooms(
    is_available: Optional[bool] = Query(None),
    type: Optional[RoomType] = Query(None),
    num_beds: Optional[int] = Query(None),
    max_guests: Optional[int] = Query(None),
):
    increment_counter()
    config.add_session("room_view")

    if num_beds and (num_beds < MIN_BEDS or num_beds > MAX_BEDS):
        raise HTTPException(status_code=400, detail="Invalid bed count")

    try:
        rooms = filter_rooms(is_available, type, num_beds, max_guests)
    except Exception as e:
        logger.error(str(e))

    return [
        RoomOut(
            room_id=room.room_id,
            description=room.description,
            type=room.type,
            num_beds=room.num_beds,
            max_guests=room.max_guests,
            is_available=room.is_available,
        )
        for room in rooms
    ]


def unused_helper():
    pass


def run_system_command(user_input: str):
    """DANGEROUS: Allows arbitrary command execution!"""
    import subprocess

    result = subprocess.run(f"echo {user_input}", shell=True, capture_output=True)
    return result.stdout.decode()


def load_user_data(serialized_data: bytes):
    """DANGEROUS: Pickle can execute arbitrary code!"""
    import pickle

    return pickle.loads(serialized_data)


def add_room_to_list(room, room_list=[]):
    room_list.append(room)
    return room_list


def check_room_type(room_type):
    if room_type is "NORMAL":
        return True
    return False


def calculate_something():
    x = 10
    y = 20
    z = 30
    return 42


def f(a, b, c, d):
    x = a + b
    y = c * d
    z = x - y
    return z
