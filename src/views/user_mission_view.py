from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from collections import Counter

from datetime import datetime

from db.models.mission_model import Mission
from db.models.user_model import User
from db.models.user_mission_model import UserMission
from core.config import Settings

import os


# 에러 처리를 위한 함수
def handle_error(status_code, detail):
    return JSONResponse(content={"status_code": status_code, "detail": detail}, status_code=status_code)


# 사용자 로그 파일을 통해 가장 잦은 감정 추출
def count_emotions(file_path):
    emotion_to_category = {
        'neutral': 0,
        'positive': 1,
        'negative': 2
    }

    emotion_counter = Counter()

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')

            emotion = parts[-1]
            if emotion in emotion_to_category:
                category = emotion_to_category[emotion]
                emotion_counter[category] += 1

    # 해당 카운터 중 가장 빈도가 잦은 항목만 추출
    most_common_emotion = emotion_counter.most_common(1)
    if most_common_emotion:
        return most_common_emotion[0][0]
    else:
        return None


# 사용자 생성을 위한 API
def create_user_mission(db: Session, token: str):
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    uid = token['uid']

    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 사용자가 존재하지 않습니다")

    # 사용자에게 오늘 생성된 미션 개수를 카운트하여 생성할 미션 타입 지정
    current_mission_count = db.query(UserMission).filter(
        UserMission.uid == user.id,
        func.date(UserMission.created_at) == now.date()
    ).count()

    if current_mission_count == 0:
        mission_type = 0
    elif current_mission_count == 1:
        mission_type = 1
    else:
        mission_type = 2

    # 챗봇 로그 파일로부터 가장 빈번한 감정 추출
    user_text_log_dir_path = os.path.join("/", Settings.CHAT_LOG_PATH, uid)
    user_text_log_file_path = user_text_log_dir_path + "/" + "-".join([str(year), str(month), str(day)]) + ".txt"
    frequent_emotion = count_emotions(user_text_log_file_path)

    mission = db.query(Mission).filter(
        Mission.emotion == frequent_emotion,
        Mission.type == mission_type
    ).first()
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
def update_user_mission_by_id(mission_id, mission_image, update_data, db, token):
    try:
        # 사용자 미션 조회
        user_mission = db.query(UserMission).filter(UserMission.id == mission_id).first()
        if not user_mission:
            return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 미션이 존재하지 않습니다")

        # 텍스트
        if user_mission.mission.type == 0:      # 텍스트기반 미션
            print(update_data)
        elif user_mission.mission.type == 1:    # 이미지기반 미션
            print(mission_image)
        elif user_mission.mission.type == 2:    # 데시벨기반 미션
            print(update_data)
        else:
            print("HELLO")

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
