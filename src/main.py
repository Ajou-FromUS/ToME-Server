"""Module for running Web Server"""
from fastapi import FastAPI
from routers.mission_router import mission
from routers.user_router import user
from routers.etc_routers import etc
from routers.chatbot_router import chatbot
from routers.user_mission_router import user_mission


def create_app() -> FastAPI:
    _app = FastAPI()

    _app.include_router(mission)
    _app.include_router(user)
    _app.include_router(user_mission)
    _app.include_router(etc)
    _app.include_router(chatbot)

    return _app


app = create_app()
