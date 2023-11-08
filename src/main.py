"""Module for running Web Server"""
from fastapi import FastAPI
from routers.mission_router import mission
from routers.user_router import user
from routers.etc_routers import etc


def create_app() -> FastAPI:
    _app = FastAPI()

    _app.include_router(mission)
    _app.include_router(user)
    _app.include_router(etc)

    return _app


app = create_app()
