from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from datetime import datetime
from redis import Redis

from db.models.mission_model import Mission
from db.models.user_model import User
from db.models.user_mission_model import UserMission


# 에러 처리를 위한 함수
def handle_error(status_code, detail):
    return JSONResponse(content={"status_code": status_code, "detail": detail}, status_code=status_code)


# 사용자 생성을 위한 API
def create_user_mission(db: Session, token: str):
    uid = token['uid']

    ''' TODO
    Redis 클라이언트로부터 사용자의 오늘 감정 기록을 가져와 해당하는 미션 객체 가져오기
    해당 날짜의 감정 기록 중 빈도가 가장 잦은 감정을 기반으로 미션 선택
    '''

    frequent_emotion = 0
    
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 사용자가 존재하지 않습니다")
    
    ''' TODO
    이미 생성된 미션일 경우, 중복 방지를 위해 해당 미션을 제외하고 나머지 미션중에서 선택해야 함
    '''

    mission = db.query(Mission).filter(Mission.emotion == frequent_emotion).first()
    if not mission:
        return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 미션이 존재하지 않습니다")

    try:
        user_mission = UserMission(
            user=user,
            mission=mission,
            content=None,
            is_completed=False,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )
        user_mission_json = jsonable_encoder(user_mission)

        db.add(user_mission)
        db.commit()
        db.refresh(user_mission)

        return JSONResponse(
            content={"status_code": status.HTTP_201_CREATED, "detail": "미션 생성 성공", "data": user_mission_json},
            status_code=status.HTTP_201_CREATED
        )
    except IntegrityError as e:
        print(e)
        db.rollback()
        return handle_error(status.HTTP_400_BAD_REQUEST, "이미 존재하는 미션입니다")
    except Exception:
        db.rollback()
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 생성 중 오류가 발생하였습니다")


# 특정 사용자의 모든 미션을 조회하기 위한 API
def get_all_user_missions_by_id(db, token):
    uid = token['uid']

    try:
        # 특정 사용자에 대해 미션에 대한 정보를 함께 반환
        missions = (db.query(UserMission)
                    .options(joinedload(UserMission.mission))
                    .join(User)
                    .filter(User.uid == uid)
                    .all())
        missions_json = jsonable_encoder(missions)

        if missions:
            return JSONResponse(
                content={"status_code": status.HTTP_200_OK, "detail": "사용자 미션 조회 성공", "data": missions_json},
                status_code=status.HTTP_200_OK
            )
        else:
            return handle_error(status.HTTP_404_NOT_FOUNT, "해당 사용자의 미션 기록이 존재하지 않습니다")
    except Exception as e:
        print(e)
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "사용자 미션 조회 중 오류가 발생하였습니다")


# 특정 사용자 + 특정 날짜의 미션을 조회하기 위한 API
def get_user_mission_by_data(date, db, token):
    uid = token['uid']

    try:
        # 문자열을 datetime 객체로 변환
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        # 특정 날짜와 사용자에 대한 UserMission 조회
        missions = (db.query(UserMission)
                    .options(joinedload(UserMission.mission))
                    .join(User)
                    .filter(User.uid == uid, func.date(UserMission.created_at) == date_obj)
                    .all())
        missions_json = jsonable_encoder(missions)

        # 항상 길이가 3인 list 형태로 반환
        while len(missions_json) < 3:
            missions_json.append({})

        if missions:
            return JSONResponse(
                content={"status_code": status.HTTP_200_OK, "detail": "사용자 미션 조회 성공", "data": missions_json},
                status_code=status.HTTP_200_OK
            )
        else:
            return handle_error(status.HTTP_404_NOT_FOUND, "해당 날짜에 대한 미션 데이터가 존재하지 않습니다")
    except Exception as e:
        print(e)
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "사용자 미션 조회 중 오류가 발생하였습니다")


# 특정 미션을 업데이트하기 위한 API
def update_user_mission_by_id(mission_id, update_data, db, token):
    try:
        user_mission = db.query(UserMission).filter(UserMission.id == mission_id).first()
        if not user_mission:
            return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 미션이 존재하지 않습니다")

        valid = False
        for key, value in update_data.items():
            if hasattr(user_mission, key):
                setattr(user_mission, key, value)
                valid = True
            else:
                return handle_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "일치하는 항목이 존재하지 않습니다")

        if valid:
            db.commit()
            db.refresh(user_mission)

            user_mission_json = jsonable_encoder(user_mission)

            return JSONResponse(
                content={"status_code": 200, "detail": f"{mission_id}번 미션 업데이트 성공", "data": user_mission_json},
                status_code=status.HTTP_200_OK
            )
    except Exception as e:
        print(e)
        db.rollback()
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 업데이트 중 오류가 발생하였습니다")
    

def delete_user_mission_by_id(mission_id, db, token):
    try:
        user_mission = db.query(UserMission).filter(UserMission.id == mission_id).first()
        if not user_mission:
            return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 미션이 존재하지 않습니다")
        
        db.delete(user_mission)
        db.commit()

        return JSONResponse(
            content={"status_code": status.HTTP_200_OK, "detail": "미션 삭제 성공"},
            status_code=status.HTTP_200_OK
        )
    except Exception:
        db.rollback()
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 삭제 중 오류가 발생하였습니다")
