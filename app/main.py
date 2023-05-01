from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import security
from app.api import points
from app.frontend import frontend
from app.lib.twitch import twitch


@asynccontextmanager
async def lifespan(app: FastAPI):
    await twitch.init()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/hello")
async def root():
    return {"message": "Hello Mundo"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


security.init(app)
points.init(app)
frontend.init(app)
