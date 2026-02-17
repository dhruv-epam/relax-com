from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import os  # Unused import
import sys  # Unused import
from app.schemas.schemas import RoomOut
from app.models.models import RoomType, Room
from app.services.services import (
    filter_rooms,
    get_available_rooms,
)  # Duplicate function import

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
