import uuid
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    twitch_id: str
    display_name: str
    profile_image_url: str
    created_at: datetime


class UserDetails(UserBase):
    id: uuid.UUID


class UserCreate(UserBase):
    token: str


class UserFull(UserDetails, UserCreate):
    pass


class PointValueBase(BaseModel):
    channel_name: str
    value: int
    date: datetime


class PointValueDetails(PointValueBase):
    id: uuid.UUID
    user: uuid.UUID

    class Config:
        orm_mode = True
