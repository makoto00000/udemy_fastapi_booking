from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class BaseUser(BaseModel):
    name: str = Field(max_length=20, examples=["テストユーザー"])


class UserCreate(BaseUser):
    pass


class UserResponse(BaseUser):
    created_at: datetime
    updated_at: datetime


class RoomCreate(BaseModel):
    name: str = Field(max_length=20, examples=["テスト部屋"])
    capacity: int = Field(gt=1, examples=[6])


class BookingCreate(BaseModel):
    reserved_num: int = Field()
    start_date_time: datetime = Field()
    end_date_time: datetime = Field()

    @model_validator(mode="before")
    def validate_times(self):
        errors = []

        start = self.start_date_time
        end = self.end_date_time

        # すべてのフィールドが存在するか確認
        if not start or not end:
            return self

        # 1. 時間が15分刻みかどうかを確認
        if start.minute % 15 != 0:
            errors.append("開始時間は15分刻みで設定してください")
        if end.minute % 15 != 0:
            errors.append("終了時間は15分刻みで設定してください")

        # 2. 9:00〜20:00の範囲内かを確認
        if not (9 <= start.hour < 20):
            errors.append("開始時間は9:00〜20:00の範囲内でなければなりません")
        if not (9 <= end.hour <= 20):
            errors.append("終了時間は9:00〜20:00の範囲内でなければなりません")

        # 3. 同じ日であるかを確認
        if start.date() != end.date():
            errors.append("予約は同じ日にち内でなければなりません")

        # 4. 開始時間が終了時間よりも前か確認
        if start >= end:
            errors.append("開始時間は終了時間よりも前でなければなりません")

        # エラーがあれば例外を発生
        if errors:
            raise ValueError(errors)

        return self
