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

    res = user_view.create_user(user_data=user_data, db=db, token=token)
    return res


# 사용자 조회를 위한 API
@user.get("")
def get_user(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = user_view.get_user_by_id(db=db, token=token)
    return res


# 사용자 업데이트를 위한 API
@user.patch("")
async def update_user(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    update_data = await request.json()

    res = user_view.update_user_by_id(update_data=update_data, db=db, token=token)
    return res


# 사용자 삭제를 위한 API
@user.delete("")
async def delete_user(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = user_view.delete_user(db=db, token=token)
    return res
