from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from db.models.mission_model import Mission


# 에러 처리를 위한 함수
def handle_error(status_code, detail):
    return JSONResponse(content={"status_code": status_code, "detail": detail}, status_code=status_code)


def create_mission(mission_data: dict, db: Session):
    # 필수 항목 누락 체크
    required_fields = ['title', 'type', 'emotion']
    if not all(field in mission_data for field in required_fields):
        return handle_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "필수 항목 중 일부가 누락되었습니다")

    try:
        # get()은 항목이 없을경우 자동으로 None으로 처리
        title = mission_data.get('title')
        type = mission_data.get('type')
        emotion = mission_data.get('emotion')
        keyword = mission_data.get('keyword')

        mission = Mission(title=title, keyword=keyword, type=type, emotion=emotion)
        mission_json = jsonable_encoder(mission)

        db.add(mission)
        db.commit()
        db.refresh(mission)

        return JSONResponse(
            content={"status_code": status.HTTP_201_CREATED, "detail": "미션 생성 성공", "data": mission_json},
            status_code=status.HTTP_201_CREATED
        )
    except IntegrityError:
        db.rollback()
        return handle_error(status.HTTP_400_BAD_REQUEST, "이미 존재하는 미션입니다")
    except Exception:
        db.rollback()
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 생성 중 오류가 발생하였습니다")


def get_all_mission(db: Session):
    try:
        missions = db.query(Mission).all()
        missions_json = jsonable_encoder(missions)

        if missions:
            return JSONResponse(
                content={"status_code": 200, "detail": "전체 미션 조회 성공", "data": missions_json},
                status_code=status.HTTP_200_OK
            )
        else:
            return handle_error(status.HTTP_404_NOT_FOUND, "미션이 존재하지 않습니다")
    except Exception:
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 조회 중 오류가 발생하였습니다")


def get_mission_by_id(mission_id: int, db: Session):
    try:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        mission_json = jsonable_encoder(mission)

        if mission:
            return JSONResponse(
                content={"status_code": 200, "detail": f"{mission_id}번 미션 조회 성공", "data": mission_json},
                status_code=status.HTTP_200_OK
            )
        else:
            return handle_error(status.HTTP_404_NOT_FOUND, f"{mission_id}번 미션이 존재하지 않습니다")
    except Exception:
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 조회 중 오류가 발생하였습니다")


def update_mission_by_id(mission_id: int, update_data: dict, db: Session):
    try:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if not mission:
            return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 미션이 존재하지 않습니다")

        # 매개변수로 넘어온 항목이 실제 데이터에 없을 경우 에러 반환
        # 존재하 경우엔 Valid를 True로 바꾼 뒤 업데이트 수행
        valid = False
        for key, value in update_data.items():
            if hasattr(mission, key):
                setattr(mission, key, value)
                valid = True
            else:
                return handle_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "일치하는 미션이 존재하지 않습니다")

        if valid:
            db.commit()
            db.refresh(mission)

            mission_json = jsonable_encoder(mission)

            return JSONResponse(
                content={"status_code": 200, "detail": f"{mission_id}번 미션 업데이트 성공", "data": mission_json},
                status_code=status.HTTP_200_OK
            )
    except Exception:
        db.rollback()
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 업데이트 중 오류가 발생하였습니다")


def delete_mission_by_id(mission_id: int, db: Session):
    try:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if not mission:
            return handle_error(status.HTTP_404_NOT_FOUND, "일치하는 미션이 존재하지 않습니다")

        db.delete(mission)
        db.commit()

        return JSONResponse(
            content={"status_code": 200, "detail": f"{mission_id}번 미션 삭제 성공"},
            status_code=status.HTTP_200_OK
        )
    except Exception:
        db.rollback()
        return handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "미션 삭제 중 오류가 발생하였습니다")
