from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now())
