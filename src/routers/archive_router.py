from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.connection import get_db
from views import archive_view

archive = APIRouter(
    prefix="/archive"
)


# 아카이브 저장을 위한 API
@archive.post("/")
async def create_archive(request: Request, db: Session = Depends(get_db)):
    archive_data = await request.json()

    res = archive_view.create_archive(archive_data=archive_data, db=db)
    return res


# 아카이브 조회를 위한 API
@archive.get("/")
def get_user(archive_id:int, user_id: int, db: Session = Depends(get_db)):
    res = archive_view.get_archive_by_id(archive_id=archive_id,user_id=user_id, db=db)
    return res


# # 사용자 업데이트를 위한 API
# @user.patch("/{user_id}")
# async def update_user(request: Request, user_id: int, db: Session = Depends(get_db)):
#     update_data = await request.json()

#     res = user_view.update_user_by_id(user_id=user_id, data=update_data, db=db)
#     return res


# # 사용자 삭제를 위한 API
# @user.delete("/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     res = user_view.delete_user(user_id=user_id, db=db)
#     return res
