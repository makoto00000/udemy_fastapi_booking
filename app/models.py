from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey,
                        CheckConstraint)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())

    bookings = relationship("Booking", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())

    bookings = relationship("Booking", back_populates="room")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    reserved_num = Column(Integer, nullable=False, default=1)
    start_date_time = Column(DateTime, nullable=False)
    end_date_time = Column(DateTime, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")

    __table_args__ = (
        # 予約する時間は15分刻みであること
        CheckConstraint(
            "EXTRACT(MINUTE FROM start_date_time) % 15 = 0 AND "
            "EXTRACT(MINUTE FROM end_date_time) % 15 = 0",
            name="check_15_minute_interval"
        ),
        # 利用時間は9:00~20:00であること
        CheckConstraint(
            "EXTRACT(HOUR FROM start_date_time) >= 9 AND "
            "EXTRACT(HOUR FROM start_date_time) < 20 AND "
            "EXTRACT(HOUR FROM end_date_time) >= 9 AND "
            "EXTRACT(HOUR FROM end_date_time) <= 20",
            name="check_time_range"
        ),
        # 開始時間と終了時間が同じ日付であること
        CheckConstraint(
            "DATE(start_date_time) = DATE(end_date_time)",
            name="check_same_day"
        ),
        # 開始時間が終了時間よりも前であること
        CheckConstraint(
            "start_date_time < end_date_time",
            name="check_start_before_end"
        ),
    )
