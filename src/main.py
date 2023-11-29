"""Module for running Web Server"""
from fastapi import FastAPI
from routers.mission_router import mission
from routers.user_router import user
from routers.etc_routers import etc
from routers.chatbot_router import chatbot
from routers.user_mission_router import user_mission

import logging
from logging.handlers import TimedRotatingFileHandler

from core.config import Settings

def create_app() -> FastAPI:
    _app = FastAPI()

    _app.include_router(mission)
    _app.include_router(user)
    _app.include_router(user_mission)
    _app.include_router(etc)
    _app.include_router(chatbot)

    return _app

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
path = Settings.LOG_PATH+"/log.txt"
handler = TimedRotatingFileHandler(path,
                                   when="d",
                                   interval=1,
                                   backupCount=60)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug('SERVER STARTED')
app = create_app()