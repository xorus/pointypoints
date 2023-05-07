from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Column, Uuid
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    """A generated user id for the app. Used for database relations and identifying an user."""
    twitch_id: Mapped[str] = mapped_column()
    """The user's Twitch ID hashed using sha256. Used for Twitch authentication."""
    date: Mapped[datetime] = mapped_column(index=True, default=datetime.utcnow)
    """App account creation date, might be useful later to find problems."""
    point_values: Mapped[List["PointValue"]] = relationship()
    token: Mapped[str] = mapped_column(index=True)
    """Randomly generated token for the user to be as some kind of password for API methods."""


class PointValue(Base):
    __tablename__ = "point_value"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    """Record identifier."""
    channel_name: Mapped[str] = mapped_column(index=True)
    """Plaintext channel name. Might be changed to a relationship to account for channel name changes."""
    value: Mapped[int] = mapped_column()
    """Point value for this record."""
    date: Mapped[datetime] = mapped_column(index=True, default=datetime.utcnow)
    """Point value date, does not have to match the record creation date (even though that is the case for now)."""
    user: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id"))
    """User who created this record."""


Index("user_point_value_channel_date", PointValue.user, PointValue.date, PointValue.channel_name)
