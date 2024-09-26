from sqlalchemy.orm import Session
from schemas import UserCreate
from models import User


def create(db: Session, user_create: UserCreate):
    new_user = User(**user_create.model_dump())
    db.add(new_user)
    db.commit()
    return new_user
