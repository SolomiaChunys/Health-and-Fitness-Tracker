from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class DailyActivityBase(BaseModel):
    steps_taken: int
    calories_burned: float
    water_intake: float
    sleep_hours: float


class DailyActivityCreate(DailyActivityBase):
    pass


class DailyActivity(DailyActivityBase):
    id: int
    date: date

    class Config:
        from_attributes = True


class DailyActivityList(BaseModel):
    activities: List[DailyActivity]


class DailyActivityUpdate(BaseModel):
    steps_taken: Optional[int] = None
    calories_burned: Optional[float] = None
    water_intake: Optional[float] = None
    sleep_hours: Optional[float] = None
