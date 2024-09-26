from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from cruds import user as user_cruds
from schemas import UserCreate, UserResponse
from database import get_db


DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=201)
async def create(db: DbDependency, user_create: UserCreate):
    return user_cruds.create(db, user_create)
