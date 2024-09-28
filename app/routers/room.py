from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from cruds import room as room_cruds
from schemas import RoomResponse, RoomCreate
from database import get_db


DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/room", tags=["Rooms"])


@router.get(
    "", response_model=list[RoomResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency):
    return room_cruds.find_all(db)


@router.post(
    "", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create(db: DbDependency, room_create: RoomCreate):
    return room_cruds.create(db, room_create)
