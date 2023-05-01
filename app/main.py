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


@app.get("/health")
async def health():
    return {"status": "OK"}


security.init(app)
points.init(app)
frontend.init(app)
