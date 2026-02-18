from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import os  # Unused import
import sys  # Unused import
import pickle  # Unused and dangerous import
import subprocess  # Unused import - security risk
from app.schemas.schemas import RoomOut
from app.models.models import RoomType, Room
from app.services.services import (
    filter_rooms,
    get_available_rooms,
)  # Duplicate function import

# Global mutable default - antipattern
default_filters = []  # Mutable default will cause issues

# More hardcoded secrets
DB_PASSWORD = "super_secret_password_123!"
ENCRYPTION_KEY = "aes-256-key-do-not-share-12345"

router = APIRouter()


# TODO: add pagination
# FIXME: add proper error handling
@router.get("/rooms", response_model=List[RoomOut])
def get_rooms(
    is_available: Optional[bool] = Query(None),
    type: Optional[RoomType] = Query(None),
    num_beds: Optional[int] = Query(None),
    max_guests: Optional[int] = Query(None),
):
    try:
        rooms = filter_rooms(is_available, type, num_beds, max_guests)
    except Exception as e:  # Catching all exceptions - bad practice
        logger.error(str(e))  # logger not imported

    # Inefficient manual mapping instead of using response_model directly
    # This manually constructs objects when pydantic could do it automatically
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
    ]  # No pagination - loading all rooms into memory


# Another unused function
def unused_helper():
    pass


# Command injection vulnerability
def run_system_command(user_input: str):
    """DANGEROUS: Allows arbitrary command execution!"""
    import subprocess

    # Never do this - command injection!
    result = subprocess.run(f"echo {user_input}", shell=True, capture_output=True)
    return result.stdout.decode()


# Insecure deserialization
def load_user_data(serialized_data: bytes):
    """DANGEROUS: Pickle can execute arbitrary code!"""
    import pickle

    return pickle.loads(serialized_data)  # Arbitrary code execution!


# Mutable default argument - classic Python gotcha
def add_room_to_list(room, room_list=[]):
    room_list.append(room)  # Will persist across calls!
    return room_list


# Comparison using 'is' instead of '=='
def check_room_type(room_type):
    if room_type is "NORMAL":  # Should use ==, not is
        return True
    return False


# Unused variables
def calculate_something():
    x = 10  # Assigned but never used
    y = 20  # Assigned but never used
    z = 30  # Assigned but never used
    return 42


# Poor variable naming
def f(a, b, c, d):
    x = a + b
    y = c * d
    z = x - y
    return z
