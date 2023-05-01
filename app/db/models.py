import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    twitch_id: Mapped[str] = mapped_column()
    display_name: Mapped[str] = mapped_column()
    profile_image_url: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(index=True, default=datetime.utcnow)
    point_values: Mapped[List["PointValue"]] = relationship()
    token: Mapped[str] = mapped_column(index=True)


class PointValue(Base):
    __tablename__ = "point_value"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    channel_name: Mapped[str] = mapped_column(index=True)
    value: Mapped[int] = mapped_column()
    date: Mapped[datetime] = mapped_column(index=True, default=datetime.utcnow)
    user: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
