from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from redis import Redis
from db.connection import get_db
from redis_client.connection import get_redis_client
from views import chat_view
from core.security import verify_token

chatbot = APIRouter(
    prefix="/chatbot"
)


# 채팅을 위한 API
@chatbot.post("")
async def chat(request: Request, db: Session = Depends(get_db), redis: Redis = Depends(get_redis_client), token: str = Depends(verify_token)):
    chat_data = await request.json()

    res = chat_view.chat(chat_data=chat_data, db=db, redis=redis, token=token)
    return res
