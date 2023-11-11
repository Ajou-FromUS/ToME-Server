from fastapi import APIRouter, Depends, Request
from redis import Redis
from redis_client.connection import get_redis_client
from views import chat_view
from core.security import verify_token

chatbot = APIRouter(
    prefix="/chatbot"
)

# 채팅을 위한 API
@chatbot.post("/")
async def chat(request: Request, redis_client: Redis = Depends(get_redis_client), token: str = Depends(verify_token)):
    chat_data = await request.json()

    res = chat_view.chat(chat_data=chat_data, redis_client=redis_client, token = token)
    return res
# @chatbot.post("/")
# async def chat(request: Request, redis_client: Redis = Depends(get_redis_client)):
#     chat_data = await request.json()

#     res = chat_view.chat(chat_data=chat_data, redis_client=redis_client)
#     return res
