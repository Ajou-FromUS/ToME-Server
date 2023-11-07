from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.connection import get_db
from views import user_view
from core.security import verify_token

user = APIRouter(
    prefix="/user"
)


# 사용자 생성을 위한 API
@user.post("")
async def create_user(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    user_data = await request.json()

    res = user_view.create_user(user_data=user_data, db=db)
    return res


# 사용자 조회를 위한 API
@user.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    res = user_view.get_user_by_id(user_id=user_id, db=db)
    return res


# 사용자 업데이트를 위한 API
@user.patch("/{user_id}")
async def update_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    update_data = await request.json()

    res = user_view.update_user_by_id(user_id=user_id, data=update_data, db=db)
    return res


# 사용자 삭제를 위한 API
@user.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    res = user_view.delete_user(user_id=user_id, db=db)
    return res
