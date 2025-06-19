from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.schemas import RoomOut
from app.models.models import RoomType, Room
from app.services.services import filter_rooms

router = APIRouter()

@router.get("/rooms", response_model=List[RoomOut])
def get_rooms(
    is_available: Optional[bool] = Query(None),
    type: Optional[RoomType] = Query(None),
    num_beds: Optional[int] = Query(None),
    max_guests: Optional[int] = Query(None),
):
    rooms = filter_rooms(is_available, type, num_beds, max_guests)
    # Convert SQLModel Room to dict for output
    return [RoomOut(
        room_id=room.room_id,
        description=room.description,
        type=room.type,
        num_beds=room.num_beds,
        max_guests=room.max_guests,
        is_available=room.is_available
    ) for room in rooms]
