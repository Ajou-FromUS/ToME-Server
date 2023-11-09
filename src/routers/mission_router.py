from fastapi import APIRouter, Request, Depends
from core.security import verify_token
from db.connection import get_db
from sqlalchemy.orm import Session
from views import mission_view

mission = APIRouter(
    prefix="/mission"
)


# 미션 생성을 위한 API
@mission.post('/')
async def create_mission(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return {'msg': '미션 생성 성공'}


# 미션 조회를 위한 API
@mission.get('/')
async def get_mission():
    return {'msg': '미션 조회 성공'}


# 미션 업데이트를 위한 API
@mission.patch('/')
async def update_mission():
    return {'msg': '미션 업데이트 성공'}


# 미션 삭제를 위한 API
@mission.delete('/')
async def delete_mission():
    return {'msg': '미션 삭제 성공'}
