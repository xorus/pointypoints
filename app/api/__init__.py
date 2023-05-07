from fastapi import FastAPI

from app.api import points, user


def init(app: FastAPI):
    points.init(app)
    user.init(app)
