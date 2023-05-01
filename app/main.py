from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app import security
from app.api import points
from app.frontend import frontend
from app.lib.twitch import twitch


@asynccontextmanager
async def lifespan(app: FastAPI):
    await twitch.init()
    yield


app = FastAPI(lifespan=lifespan)

app.mount('/userscript', StaticFiles(directory=Path(__file__).parent.parent.joinpath('userscript/build')), name='userscript')


@app.get("/health")
async def health():
    return {"status": "OK"}


security.init(app)
points.init(app)
frontend.init(app)
