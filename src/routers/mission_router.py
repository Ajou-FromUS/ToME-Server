from fastapi import APIRouter, Request, Depends
from core.security import verify_token
from db.connection import get_db
from sqlalchemy.orm import Session
from views import mission_view

mission = APIRouter(
    prefix="/mission"
)


# 미션 생성을 위한 API
@mission.post("")
async def create_mission(request: Request, db: Session = Depends(get_db)):
    mission_data = await request.json()

    res = mission_view.create_mission(mission_data=mission_data, db=db)
    return res


# 전체 미션 조회를 위한 API
@mission.get("")
def get_all_mission(request: Request, db: Session = Depends(get_db)):
    res = mission_view.get_all_mission(db=db)
    return res


# 특정 미션 조회를 위한 API
@mission.get("/{mission_id}")
def get_mission(mission_id: int, request: Request, db: Session = Depends(get_db)):
    res = mission_view.get_mission_by_id(mission_id=mission_id, db=db)
    return res


# 미션 업데이트를 위한 API
@mission.patch("/{mission_id}")
async def update_mission(mission_id: int, request: Request, db: Session = Depends(get_db)):
    update_data = await request.json()

    res = mission_view.update_mission_by_id(mission_id=mission_id, update_data=update_data, db=db)
    return res


# 미션 삭제를 위한 API
@mission.delete("/{mission_id}")
async def delete_mission(mission_id: int, request: Request, db: Session = Depends(get_db)):
    res = mission_view.delete_mission_by_id(mission_id=mission_id, db=db)
    return res
