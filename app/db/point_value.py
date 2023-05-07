import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_point_values_by_user_and_channel_name(channel_name: str, user: uuid.UUID, db: Session):
    return db.query(models.PointValue) \
        .filter(models.PointValue.user == user) \
        .filter(models.PointValue.channel_name == channel_name) \
        .limit(100).all()


def create_point_value(item: schemas.PointValueBase, user: models.User, db: Session):
    db_item = models.PointValue(**item.dict(), id=uuid.uuid1(), user=user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# list unique channels for a user
def get_unique_channels(user: uuid.UUID, db: Session):
    st = select(models.PointValue.channel_name).where(models.PointValue.user == user).distinct()
    return db.scalars(st).all()


# list unique channels for a user
def get_newest_entry(user: uuid.UUID, channel: str, db: Session):
    st = select(models.PointValue) \
        .where(models.PointValue.user == user) \
        .where(models.PointValue.channel_name == channel) \
        .order_by(models.PointValue.date.desc()) \
        .limit(1)
    return db.scalar(st)


def get_points_from_to(user: uuid.UUID, channel: str, date_from: datetime.datetime, date_to: datetime.datetime,
                       db: Session):
    st = select(models.PointValue.value, models.PointValue.date) \
        .where(models.PointValue.user == user) \
        .where(models.PointValue.channel_name == channel) \
        .where(models.PointValue.date >= date_from) \
        .where(models.PointValue.date <= date_to) \
        .order_by(models.PointValue.date.desc())
    return db.execute(st).fetchall()
