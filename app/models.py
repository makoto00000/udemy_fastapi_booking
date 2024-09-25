from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
