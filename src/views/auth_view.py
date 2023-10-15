from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from jose import JWTError, jwt
from typing import Optional
from core.config import settings


# JWT 검증 함수
def verify_jwt(token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid JWT",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise credentials_exception


# '/users/money' 엔드포인트 핸들러
# @app.get('/users/money', response_model=MoneyResponse)
# async def get_user_money(token: str = Depends(verify_jwt)):
#     return {"money": 50000}
