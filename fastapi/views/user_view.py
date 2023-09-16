from sqlalchemy.orm import Session
from fastapi import HTTPException, Response
from datetime import datetime
from db.models.user_model import User


# 사용자 생성을 위한 API
def create_user(user_data, db: Session):
    required_fields = ['user_id', 'nickname', 'access_token', 'refresh_token']
    if not all(field in user_data for field in required_fields):
        raise HTTPException(detail="입력값에 빈 항목이 있습니다", status_code=400)

    try:
        user = User(
            user_id=user_data['user_id'],
            nickname=user_data['nickname'],
            milestone=0,
            current_character_id=0,
            current_character_exp=0,
            snack_num=0,
            access_token=user_data['access_token'],
            refresh_token=user_data['refresh_token'],
            created_at=datetime.now(),
            modified_at=datetime.now(),
            last_connection=datetime.now()
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception:
        return None


# 사용자 조회를 위한 API
# 일치하는 사용자가 없을 경우 None 반환
def get_user_by_id(user_id, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


# 사용자 업데이트를 위한 API
def update_user_by_id(user_id: int, data: dict, db: Session):
    user = get_user_by_id(user_id, db)

    if user is not None:
        for key, value in data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user
    else:
        return None


# 사용자 삭제를 위한 API
def delete_user(db: Session, user_id: int):
    user = get_user_by_id(user_id, db)

    if user:
        db.delete(user)
        db.commit()
        return user
    else:
        return None
