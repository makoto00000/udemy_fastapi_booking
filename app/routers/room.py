from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from cruds import room as room_cruds
from schemas import RoomResponse, RoomCreate
from database import get_db


DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/room", tags=["Rooms"])


@router.post("", response_model=RoomResponse, status_code=201)
async def create(db: DbDependency, room_create: RoomCreate):
    return room_cruds.create(db, room_create)
