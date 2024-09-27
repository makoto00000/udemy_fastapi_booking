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

    # チェック制約
    __table_args__ = (
        # 15分間隔チェック
        CheckConstraint(
            "CAST(strftime('%M', start_date_time) AS INTEGER) % 15 = 0 AND "
            "CAST(strftime('%M', end_date_time) AS INTEGER) % 15 = 0",
            name='check_15_minute_interval'
        ),
        # 営業時間内のチェック（9時から20時の範囲内）
        CheckConstraint(
            "CAST(strftime('%H', start_date_time) AS INTEGER) >= 9 AND "
            "CAST(strftime('%H', start_date_time) AS INTEGER) < 20 AND "
            "CAST(strftime('%H', end_date_time) AS INTEGER) >= 9 AND "
            "CAST(strftime('%H', end_date_time) AS INTEGER) <= 20",
            name='check_time_range'
        ),
        # 同じ日であることのチェック
        CheckConstraint(
            "DATE(start_date_time) = DATE(end_date_time)",
            name='check_same_day'
        ),
        # 開始時間が終了時間より前であることのチェック
        CheckConstraint(
            "start_date_time < end_date_time",
            name='check_start_before_end'
        ),
    )
