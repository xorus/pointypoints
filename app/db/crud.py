import uuid

from sqlalchemy.orm import Session

from . import models, schemas


def get_point_values_by_channel_name(channel_name: str, db: Session):
    return db.query(models.PointValue).filter(models.PointValue.channel_name == channel_name).limit(100).all()


def create_point_value(item: schemas.PointValueBase, db: Session):
    db_item = models.PointValue(**item.dict(), id=uuid.uuid1())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
