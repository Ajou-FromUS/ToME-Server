from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc, asc
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from collections import Counter

from datetime import datetime, timedelta

from db.models.mission_model import Mission
from db.models.user_model import User
from db.models.user_mission_model import UserMission
from views.etc_view import classify_image_by_imagenet
from core.config import Settings

import os
import boto3
import hashlib


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

    if mission_type == 1:
        mission = db.query(Mission).filter(
            Mission.type == mission_type
        ).order_by(func.random()).first()
    else:
        mission = db.query(Mission).filter(
            Mission.emotion == frequent_emotion,
            Mission.type == mission_type
        ).order_by(func.random()).first()
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
            return handle_error(status.HTTP_404_NOT_FOUND, "해당 사용자의 미션 기록이 존재하지 않습니다")
    except Exception as e:
        print(e)
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "사용자 미션 조회 중 오류가 발생하였습니다")


# 특정 사용자 + 특정 날짜의 미션을 조회하기 위한 API
def get_user_mission_by_data(date, db, token):
    uid = token['uid']

    try:
        try:
            # 입력받은 date 매개변수를 YYYY-MM-DD로 변환 시도
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            date_filter = func.date(UserMission.created_at) == date_obj

            missions = (db.query(UserMission)
                        .options(joinedload(UserMission.mission))
                        .join(User)
                        .filter(User.uid == uid, date_filter)
                        .order_by(asc(UserMission.is_completed))
                        .all())
            missions_json = jsonable_encoder(missions)

            # 항상 길이가 3인 list 형태로 반환
            while len(missions_json) < 3:
                missions_json.append({})

        except ValueError:
            # 위 변환이 실패할 경우, YYYY-MM로 변환 시도
            date_obj = datetime.strptime(date, "%Y-%m")
            month_start = date_obj.replace(day=1)
            month_end = date_obj.replace(day=1).replace(month=date_obj.month % 12 + 1) - timedelta(days=1)
            date_filter = func.date(UserMission.created_at).between(month_start, month_end)

            missions = (db.query(UserMission)
                        .options(joinedload(UserMission.mission))
                        .join(User)
                        .filter(User.uid == uid, date_filter)
                        .order_by(UserMission.created_at.desc())
                        .all())
            missions_json = jsonable_encoder(missions)

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

        valid = False

        # 텍스트 & 데시벨 기반 미션
        if user_mission.mission.type == 0 or user_mission.mission.type == 2:
            if 'content' in update_data:
                user_mission.content = update_data['content']
                user_mission.is_completed = True
                valid = True
            else:
                return handle_error(status.HTTP_400_BAD_REQUEST, "content 항목이 입력되지 않았습니다")

        # 이미지 기반 미션
        elif user_mission.mission.type == 1:
            # 키워드가 존재하는 미션일 경우 이미지 분석 실행
            if user_mission.mission.keyword:
                labels = classify_image_by_imagenet(mission_image)
                keyword = user_mission.mission.keyword.lower()

                # 이미지 분석을 통한 labels 안에 keyword가 존재하는지 확인
                if any(keyword in label.lower() for label in labels):
                    image_path = upload_image_to_s3(token['uid'],mission_image)
                    user_mission.content = image_path
                    user_mission.is_completed = True
                    valid = True
                else:
                    return handle_error(status.HTTP_400_BAD_REQUEST, f"올바르지 않은 이미지입니다. 해당 이미지는 {labels}를 포함하고 있습니다")
            # 키워드가 필요하지 않은 미션일 경우 통과
            else:
                image_path = upload_image_to_s3(token['uid'], mission_image)
                user_mission.content = image_path
                user_mission.is_completed = True
                valid = True

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


def upload_image_to_s3(uid: str, image):
    s3_client = boto3.client('s3',
                             aws_access_key_id=Settings.S3_ACCESS_KEY,
                             aws_secret_access_key=Settings.S3_SECRET_KEY,
                             region_name=Settings.S3_REGION)
    m = hashlib.sha256()
    m.update(uid.encode())
    m.update(str(datetime.now()).encode())
    img_name = m.hexdigest()
    s3_client.put_object(Body=image,Bucket=Settings.S3_BUCKET_NAME,Key="img/"+img_name+".jpeg")
    s3_path = "https://fromus-tome.s3.ap-northeast-2.amazonaws.com/img/"+img_name+".jpeg"
    return s3_path