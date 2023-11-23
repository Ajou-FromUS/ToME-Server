from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from core.security import verify_token
from db.connection import get_db
from sqlalchemy.orm import Session
from views import user_mission_view
from typing import Optional

import json

user_mission = APIRouter(
    prefix="/user/mission"
)


# 사용자별 미션 생성을 위한 API
# 채팅 대화 누적 기록이 일정 횟수 이상일때마다 해당 함수를 호출하여 사용자별 미션 생성
@user_mission.post("")
def create_user_mission(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = user_mission_view.create_user_mission(db=db, token=token)
    return res


# 사용자별 모든 미션 조회를 위한 API
@user_mission.get("")
def get_all_user_missions_by_id(request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = user_mission_view.get_all_user_missions_by_id(db=db, token=token)
    return res


# 특정 날짜의 사용자의 미션 기록을 조회하기 위한 API
@user_mission.get("/{date}")
def get_user_mission_by_data(date: str, request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = user_mission_view.get_user_mission_by_data(date=date, db=db, token=token)
    return res


# 사용자별 미션 업데이트를 위한 API
@user_mission.patch("/{mission_id}")
async def update_user_mission_by_id(mission_id: int, request: Request, db: Session = Depends(get_db), 
                                    token: str = Depends(verify_token), mission_image: Optional[UploadFile] = File(None)):
    # 초기 데이터 조회
    try:
        update_data = await request.json()
    except json.JSONDecodeError:
        update_data = {}

    image_data = None
    if mission_image:
        image_data = await mission_image.read()

    res = user_mission_view.update_user_mission_by_id(
            mission_id=mission_id, mission_image=image_data,
            update_data=update_data, db=db, token=token
        )
    return res


# 특정 미션 삭제를 위한 API
@user_mission.delete("/{mission_id}")
def delete_user_mission_by_id(mission_id: int, request: Request, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    res = user_mission_view.delete_user_mission_by_id(mission_id=mission_id, db=db, token=token)
    return res
