import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, text, func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base


# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Uuid, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")

class PointValue(Base):
    __tablename__ = "point_value"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True)
    channel_name: Mapped[str] = mapped_column(index=True)
    value: Mapped[int] = mapped_column()
    date: Mapped[datetime] = mapped_column(index=True, default=func.now)
