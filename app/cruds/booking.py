from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Booking, Room
from schemas import BookingCreate, BookingValidationMessages


def create(db: Session, booking_create: BookingCreate,
           user_id: int, room_id: int):
    # 予約人数がroomのcapacity以下かバリデーション
    room = db.query(Room).filter(Room.id == room_id).first()
    if room.capacity < booking_create.reserved_num:
        raise HTTPException(status_code=422, detail=(
            BookingValidationMessages.OVER_CAPACITY.value))

    new_booking = Booking(
        **booking_create.model_dump(), user_id=user_id, room_id=room_id)
    db.add(new_booking)
    db.commit()
    return new_booking
