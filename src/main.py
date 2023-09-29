"""Module for running Web Server"""
from fastapi import FastAPI
from routers.archive_router import archive
from routers.character_router import character
from routers.diary_router import diary
from routers.mission_router import mission
from routers.user_router import user
from routers.etc_routers import etc


def create_app() -> FastAPI:
    _app = FastAPI()

    _app.include_router(archive)
    _app.include_router(character)
    _app.include_router(diary)
    _app.include_router(mission)
    _app.include_router(user)
    _app.include_router(etc)

    return _app


app = create_app()
