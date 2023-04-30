import uuid
from datetime import datetime

from pydantic import BaseModel


class PointValueBase(BaseModel):
    channel_name: str
    value: int
    date: datetime


class PointValue(PointValueBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
