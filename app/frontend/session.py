import uuid

from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.db import models


class SessionData(BaseModel):
    user_id: str | None
    display_name: str | None
    profile_image_url: str | None


def is_logged_in(request: Request):
    if request.session is None:
        return False
    return SessionData(**request.session).user_id is not None


def get_session_info(request: Request) -> SessionData | None:
    if request.session is None or 'user_id' not in request.session:
        return None
    return SessionData(**request.session)


def get_session_user(request: Request, db: Session):
    if request.session is None:
        return None

    user_id = SessionData(**request.session).user_id
    if user_id is None:
        return None

    return db.query(models.User).filter(models.User.id == uuid.UUID(user_id)).first()


def set_session_from_user(request: Request, user_id: uuid.UUID, display_name: str, profile_image_url: str):
    request.session.update({
        'user_id': str(user_id),
        'display_name': display_name,
        'profile_image_url': profile_image_url
    })


def session_clear(request: Request):
    request.session.clear()
