import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from app.db.database import get_db
from app.db.schemas import UserFull
from app.db.user import get_user
from app.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

JWT_ALGORITHM = "HS256"


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[JWT_ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception

    except JWTError as e:
        print(e)
        raise credentials_exception
    user = get_user(uuid.UUID(sub), db)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(user_id: uuid.UUID, user_name: str):
    return jwt.encode(
        {
            "sub": str(user_id),
            "name": user_name,
            "iat": datetime.utcnow()
        },
        settings.jwt_secret,
        JWT_ALGORITHM
    )


RequireUserToken = Annotated[UserFull, Depends(get_current_user)]
