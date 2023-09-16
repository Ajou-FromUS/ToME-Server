from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from views import user_view

user = APIRouter(
    prefix="/user"
)


# 사용자 생성을 위한 API
@user.post("/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    user = user_view.create_user(user_data=user_data, db=db)

    if user is not None:
        return {"status_code": 200,
                "message": "사용자 생성 성공",
                "data": user}
    else:
        return {"status_code": 500,
                "message": "사용자 생성 실패"}


# 사용자 조회를 위한 API
@user.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_view.get_user_by_id(user_id=user_id, db=db)

    if user is not None:
        return {"status_code": 200,
                "message": "사용자 조회 성공",
                "data": user}
    else:
        return {"status_code": 500,
                "message": "사용자 조회 실패"}


# 사용자 업데이트를 위한 API
@user.patch("/{user_id}")
async def update_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    update_data = await request.json()
    user = user_view.update_user_by_id(user_id=user_id, data=update_data, db=db)

    if user is not None:
        return {"status_code": 200,
                "message": "사용자 업데이트 성공",
                "data": user}
    else:
        return {"status_code": 500,
                "message": "사용자 업데이트 실패"}


# 사용자 삭제를 위한 API
@user.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_view.delete_user(user_id=user_id, db=db)

    if user is not None:
        return {"status_code": 200,
                "message": "사용자 삭제 성공",
                "data": user}
    else:
        return {"status_code": 400,
                "message": "사용자 삭제 실패"}
