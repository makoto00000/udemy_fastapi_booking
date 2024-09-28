from datetime import datetime
from enum import Enum
from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator


# User
class BaseUser(BaseModel):
    name: str = Field(max_length=20, examples=["テストユーザー"])


class UserCreate(BaseUser):
    pass


class UserResponse(BaseUser):
    created_at: datetime
    updated_at: datetime


# Room
class RoomBase(BaseModel):
    name: str = Field(max_length=20, examples=["テスト部屋"])
    capacity: int = Field(ge=1, examples=[6])


class RoomCreate(RoomBase):
    pass


class RoomResponse(RoomBase):
    created_at: datetime
    updated_at: datetime


# Booking
class BookingBase(BaseModel):
    reserved_num: int = Field(examples=[1])
    start_date_time: datetime = Field(examples=["2020-01-01T09:00:00"])
    end_date_time: datetime = Field(examples=["2020-01-01T12:00:00"])


class BookingValidationMessages(Enum):
    INVALID_MINUTE = "時間は15分刻みで設定してください"
    OUT_OF_HOURS = "時間は9:00〜20:00の範囲内でなければなりません"
    DIFFERENT_DAYS = "予約は同じ日にち内でなければなりません"
    START_AFTER_END = "開始時間は終了時間よりも前でなければなりません"
    OVER_CAPACITY = "予約人数が部屋の定員を超えています"


class BookingCreate(BookingBase):

    @model_validator(mode="before")
    def validate_times(cls, values):
        errors = []

        start = datetime.fromisoformat(values.get("start_date_time"))
        end = datetime.fromisoformat(values.get("end_date_time"))

        # すべてのフィールドが存在するか確認
        if not start or not end:
            return values

        # 1. 時間が15分刻みかどうかを確認
        if start.minute % 15 != 0:
            errors.append(BookingValidationMessages.INVALID_MINUTE.value)
        if end.minute % 15 != 0:
            errors.append(BookingValidationMessages.INVALID_MINUTE.value)

        # 2. 9:00〜20:00の範囲内かを確認
        if not (9 <= start.hour < 20):
            errors.append(BookingValidationMessages.OUT_OF_HOURS.value)
        if not (9 <= end.hour <= 20):
            errors.append(BookingValidationMessages.OUT_OF_HOURS.value)

        # 3. 同じ日であるかを確認
        if start.date() != end.date():
            errors.append(BookingValidationMessages.DIFFERENT_DAYS.value)

        # 4. 開始時間が終了時間よりも前か確認
        if start >= end:
            errors.append(BookingValidationMessages.START_AFTER_END.value)

        # エラーがあれば例外を発生
        if errors:
            raise HTTPException(
                status_code=422, detail=errors)

        return values


class BookingResponse(BookingBase):
    user_id: int
    room_id: int
    created_at: datetime
    updated_at: datetime
