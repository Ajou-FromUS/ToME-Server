from PIL import Image
from io import BytesIO
from fastapi import Request, status
from fastapi.responses import JSONResponse
from datetime import date, timedelta, datetime
from google.cloud import vision
from dotenv import load_dotenv
from collections import Counter

from db.models.user_model import User
from db.models.user_mission_model import UserMission
from core.config import Settings

import os
import json
import tempfile
import requests
import glob
import calendar

load_dotenv()


def init_client(request, db, token):
    user = db.query(User).filter(User.uid == token['uid']).first()

    today = date.today()

    today_mission_count = db.query(UserMission).filter(
        UserMission.uid == user.id,
        UserMission.created_at >= today,
        UserMission.created_at < today + timedelta(days=1)
    ).count()
    has_mission_today = today_mission_count > 0

    data = {
        "nickname": user.nickname,
        "has_mission_today": has_mission_today
    }

    return JSONResponse(
        content={"status_code": status.HTTP_200_OK, "detail": "초기 데이터 조회 성공", "data": data},
        status_code=status.HTTP_200_OK
    )


def get_monthly_log_by_user(date, db, token):
    uid = token['uid']
    user = db.query(User).filter(User.uid == uid).first()

    # 채팅 워드클라우드 이미지
    keyword_cloud_image_url = Settings.S3_BUCKET_URL + uid + '/' + date + ".png"

    # 월간 감정 백분위
    # date를 통해 'year-month' prefix와 일치하는 모든 텍스트파일을 읽어와 총 감정 개수 카운트
    year, month = date.split('-')

    user_text_log_dir_path = os.path.join("/", Settings.CHAT_LOG_PATH, uid)

    file_pattern = os.path.join(user_text_log_dir_path, f"{year}-{month}-*.txt")
    log_files = glob.glob(file_pattern)

    emotion_counter = Counter()

    # prefix와 일치하는 모든 파일들을 순회
    for file_path in log_files:
        emotion_counter = count_emotions(emotion_counter, file_path)

    # 감정 갯수를 백분위로 환산
    total_emotions = sum(emotion_counter.values())
    emotion_percentages = {emotion: (count / total_emotions) for emotion, count in emotion_counter.items()}

    # 월간 미션 수행 현황 (개수로 표현)
    year, month = map(int, date.split('-'))
    num_days = calendar.monthrange(year, month)[1]

    # 전체 미션 완료 횟수를 누적하기 위한 리스트
    # 날짜수에 맞게끔 초기 리스트를 0으로 초기화하여 생성
    completed_mission_counts = [0] * num_days

    # 전체 미션들 중 입력받은 월에 포함되며 완료된 미션들을 조회
    completed_missions = db.query(UserMission).filter(
        UserMission.uid == user.id,
        UserMission.is_completed == True,
        UserMission.created_at >= datetime(year, month, 1),
        UserMission.created_at < datetime(year, month + 1, 1)
    ).all()

    # 완료된 미션들을 순회하여 해당 날짜에 해당하는 리스트의 값을 1씩 누적
    for mission in completed_missions:
        day_completed = mission.created_at.day
        completed_mission_counts[day_completed - 1] += 1

    data = {
        "keyword_cloud_image_url": keyword_cloud_image_url,
        "emotion_percentages": emotion_percentages,
        "completed_mission_counts": completed_mission_counts
    }

    return JSONResponse(
                content={"status_code": status.HTTP_200_OK, "detail": "월간 통계 기록 조회 성공", "data": data},
                status_code=status.HTTP_200_OK
            )


def refresh_token(request):
    access_token = request.headers['access_token']
    refresh_token = request.headers['refresh_token']

    url = 'https://api.furo.one/sessions/token/refresh'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {refresh_token}'
    }
    data = {'accessToken': access_token}
    response = requests.post(url, headers=headers, json=data)

    new_token = response.json().get('access_token')
    return {'access_token': new_token} if new_token else None


# 이미지 분류 함수 정의
def classify_image_by_imagenet(image):
    # .env 파일로부터 서비스 키 추출
    service_key_string = os.getenv('GOOGLE_SERVICE_KEY')
    service_key = json.loads(service_key_string)

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        json.dump(service_key, temp_file)
        temp_file_path = temp_file.name

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    label_descriptions = [label.description for label in labels]

    os.remove(temp_file_path)

    return label_descriptions


def count_emotions(emotion_counter, file_path):
    emotion_to_category = {
        'neutral': 0,
        'positive': 1,
        'negative': 2
    }

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            emotion = parts[-1]
            if emotion in emotion_to_category:
                emotion_counter[emotion] += 1

    return emotion_counter
