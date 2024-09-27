from sqlalchemy.orm import Session
from models import Room
from schemas import RoomCreate


def create(db: Session, room_create: RoomCreate):
    new_room = Room(**room_create.model_dump())
    db.add(new_room)
    db.commit()
    return new_room
