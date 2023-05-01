from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db import schemas, point_value
from app.db.database import get_db
from app.lib.auth import RequireUserToken


def init(app: FastAPI) -> None:
    @app.post('/points', response_model=schemas.PointValueDetails)
    async def create_points(pv: schemas.PointValueBase, user: RequireUserToken, db: Session = Depends(get_db)):
        return point_value.create_point_value(pv, user, db)

    @app.get('/points/{channel_name}', response_model=list[schemas.PointValueDetails])
    async def get_points(channel_name: str, user: RequireUserToken, db: Session = Depends(get_db)):
        return point_value.get_point_values_by_user_and_channel_name(channel_name, user.id, db)
