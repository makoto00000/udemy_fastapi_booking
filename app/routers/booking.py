from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from schemas import BookingCreate, BookingResponse
from cruds import booking as booking_cruds


router = APIRouter(prefix="/booking", tags=["Bookings"])

DbDependency = Annotated[Session, Depends(get_db)]


@router.get(
    "", response_model=list[BookingResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency):
    return booking_cruds.find_all(db)


@router.post(
    "", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create(db: DbDependency, booking_create: BookingCreate,
                 user_id: int, room_id: int):
    return booking_cruds.create(db, booking_create, user_id, room_id)
