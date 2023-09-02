from fastapi import FastAPI
from routers.archive_router import archive
from routers.character_router import character
from routers.diary_router import diary
from routers.mission_router import mission
from routers.user_router import user
from routers.etc_routers import etc

app = FastAPI()

app.include_router(archive)
app.include_router(character)
app.include_router(diary)
app.include_router(mission)
app.include_router(user)
app.include_router(etc)


# @app.get("/")
# async def home():
#     return "Hello World"
