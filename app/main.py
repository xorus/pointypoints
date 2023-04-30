from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import frontend
from app.db import schemas, crud
from app.db.get_db import get_db

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello Mundo"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post('/points', response_model=schemas.PointValue)
async def create_points(pv: schemas.PointValueBase, db: Session = Depends(get_db)):
    return crud.create_point_value(pv, db)


@app.get('/points/{channel_name}', response_model=list[schemas.PointValue])
async def get_points(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_point_values_by_channel_name(channel_name, db)


frontend.init(app)
