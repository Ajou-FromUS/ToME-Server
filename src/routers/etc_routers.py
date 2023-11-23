from fastapi import APIRouter, Request, UploadFile, Depends
from sqlalchemy.orm import Session

from db.connection import get_db
from core.security import verify_token

from views import etc_view

etc = APIRouter()


# 애플리케이션 로딩시 필요 데이터를 조회하기 위한 API
@etc.get('/')
async def init_client(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = etc_view.init_client(request, db, token)
    return res


# 사용자의 월간 활동기록을 조회하기 위한 API
@etc.get('/statistics/{date}')
def get_monthly_log_by_user(date: str, request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = etc_view.get_monthly_log_by_user(date, db, token)
    return res


# 사용자의 Toekn을 재발급하기 위한 API
@etc.get('/refresh-token')
async def refresh_user_token(request: Request):
    res = etc_view.refresh_token(request)
    return res


# 이미지 디텍션을 위한 API
@etc.post('/classify')
async def classify_image(request: Request, file: UploadFile):
    image = await file.read()

    etc_view.classify_image_by_imagenet(image)
