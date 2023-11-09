from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from db.models.mission_model import Mission


# 미션 생성을 위한 API
def create_mission(mission_data: dict, db: Session):
    # 필수 항목 누락 체크
    required_fields = ['title', 'type', 'emotion']
    if not all(field in mission_data for field in required_fields):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="필수 항목 중 일부가 누락되었습니다")

    try:
        title = mission_data['title']
        type = mission_data['type']
        emotion = mission_data['emotion']

        # content 항목이 올 경우를 체크하여 동적으로 데이터 생성
        if 'content' in mission_data:
            content = mission_data['content']
            mission = Mission(title=title, content=content, type=type, emotion=emotion)
        else:
            mission = Mission(title=title, type=type, emotion=emotion)

        db.add(mission)
        db.commit()
        db.refresh(mission)

        return {
            "status_code": status.HTTP_201_CREATED,
            "detail": "미션 생성 성공",
            "data": mission
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="이미 존재하는 미션입니다")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="미션 생성 중 서버에 오류가 발생하였습니다")


# 전체 미션 조회를 위한 API
def get_all_mission(db: Session):
    missions = db.query(Mission).all()

    if missions is not None:
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "미션 조회 성공",
            "data": missions
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="미션이 존재하지 않습니다")


# 특정 미션 조회를 위한 API
def get_mission_by_id(mission_id: int, db: Session):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()

    if mission is not None:
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "미션 조회 성공",
            "data": mission
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="일치하는 미션이 존재하지 않습니다")


# 미션 업데이트를 위한 API
def update_mission_by_id(mission_id: int, update_data: dict, db: Session):
    mission = get_mission_by_id(mission_id, db)['data']
    valid = False

    # 일치하는 항목이 사용자 모델에 존재하는지 체크
    for key, value in update_data.items():
        if hasattr(mission, key):
            setattr(mission, key, value)
            valid = True
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="일치하는 항목이 존재하지 않습니다"
            )

    # 존재할 경우 업데이트 수행
    if valid is True:
        db.commit()
        db.refresh(mission)

        return {
            "status_code": status.HTTP_200_OK,
            "detail": "미션 업데이트 성공",
            "data": mission
        }


# 미션 삭제를 위한 API
def delete_mission_by_id(mission_id: int, db: Session):
    mission = get_mission_by_id(mission_id, db)['data']

    db.delete(mission)
    db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "detail": f"{mission_id}번 미션 삭제 성공",
    }
