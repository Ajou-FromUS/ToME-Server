from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from redis import Redis
from bardapi import BardCookies
from datetime import datetime
from pathlib import Path

from core.config import Settings
from views.user_mission_view import create_user_mission
from db.models.user_model import User
from db.models.user_mission_model import UserMission

import time
import traceback
import requests
import json


# 채팅 답변 요청
def chat(chat_data: dict, db: Session, redis: Redis, token: str):
    uid = token['uid']

    # 필수 항목 누락 체크
    required_fields = ['content']
    if not all(field in chat_data for field in required_fields):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="필수 항목 중 일부가 누락되었습니다")

    if chat_data.get('content') is None:
        mission_count = get_mission_count(db, uid)

        return {
            "status_code": status.HTTP_200_OK,
            "detail": "사용자 미션 개수 조회 성공",
            "mission_count": mission_count
        }

    try:
        cookie_dict = redis.hgetall('cookies')

        bard = BardCookies(cookie_dict=cookie_dict)
        user_text = chat_data['content']
        input_text = Settings.CHAT_INPUT_TEXT + user_text

        start_time = time.time()
        response = bard.get_answer(input_text)['content']
        end_time = time.time()
        elapsed_time = end_time-start_time

        start_idx = response.find('[')
        end_idx = response.find(']')
        answer = response[start_idx+1:end_idx]

        # Naver Clova Sentiment
        clova_base_url = Settings.CLOVA_BASE_URL
        clova_request_headers = {
            "X-NCP-APIGW-API-KEY-ID": Settings.CLOVA_API_KEY_ID,
            "X-NCP-APIGW-API-KEY": Settings.CLOVA_API_KEY,
            "Content-Type": "application/json"
        }
        clova_data = {
            "content": user_text
        }

        clova_response = requests.post(url=clova_base_url, json=clova_data, headers=clova_request_headers)
        clova_content = json.loads(clova_response.text)
        sentiment = clova_content['document']['sentiment']

        print(f"uid: {uid} Elapsed Time: {elapsed_time} Input Text: {user_text} Output Text: {answer} Clova Answer: {sentiment}")

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        user_text_log_dir_path = "/".join([Settings.CHAT_LOG_PATH,uid])
        user_text_log_file_path = user_text_log_dir_path+"/"+"-".join([str(year), str(month), str(day)])+".txt"
        Path(user_text_log_dir_path).mkdir(parents=True, exist_ok=True)
        user_text_log_file = open(user_text_log_file_path, mode="a+t")
        user_text_log_file.write(" - ".join([now.ctime(), user_text, sentiment]) + "\n")
        user_text_log_file.close()

        # 사용자가 응답을 5회 할때마다 새로운 미션 생성
        user_text_log_file = open(user_text_log_file_path, mode="r")
        line_count = len(user_text_log_file.readlines())
        mission_count = get_mission_count(db, uid)

        if mission_count < 3 and line_count % 5 == 0:
            create_user_mission(db, token)

        return {
            "status_code": status.HTTP_200_OK,
            "detail": "채팅 답변 생성 성공",
            "message": answer,
            "mission_count": mission_count
        }
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="채팅 답변 생성 중 서버에 오류가 발생하였습니다")


# 사용자의 현재 미션 개수를 조회하기 위한 함수
def get_mission_count(db, uid):
    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")
    mission_count = db.query(func.count(UserMission.id)) \
                        .join(User) \
                        .filter(User.uid == uid, func.date(UserMission.created_at) == current_date) \
                        .scalar()

    return mission_count
