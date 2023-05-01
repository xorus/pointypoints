import uuid
from secrets import token_urlsafe

from sqlalchemy.orm import Session

from . import models, schemas


def create_user_from_twitch(twitch_id: str, display_name: str, profile_image_url: str, db: Session) -> schemas.UserFull:
    db_item = models.User(
        id=uuid.uuid4(),
        token=token_urlsafe(64),
        twitch_id=twitch_id,
        display_name=display_name,
        profile_image_url=profile_image_url,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user_by_twitch_id(twitch_id: str, db: Session) -> schemas.UserFull | None:
    return db.query(models.User).filter(models.User.twitch_id == twitch_id).first()


def update_existing_token_and_info(user: schemas.UserFull, db: Session) -> schemas.UserFull:
    user.token = token_urlsafe(64)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(sub: uuid.UUID, db: Session) -> schemas.UserFull | None:
    return db.query(models.User).filter(models.User.id == sub).first()
