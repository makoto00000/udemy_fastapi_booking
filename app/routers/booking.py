from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import BookingCreate, BookingResponse
from cruds import booking as booking_cruds


router = APIRouter(prefix="/booking", tags=["Bookings"])

DbDependency = Annotated[Session, Depends(get_db)]


@router.post("", response_model=BookingResponse, status_code=201)
async def create(db: DbDependency, booking_create: BookingCreate,
                 user_id: int, room_id: int):
    return booking_cruds.create(db, booking_create, user_id, room_id)
