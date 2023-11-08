from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
from db.models.user_model import User


# 사용자 생성을 위한 API
def create_user(user_data: dict, db: Session, token: str):
    # 필수 항목 누락 체크
    required_fields = ['nickname']
    if not all(field in user_data for field in required_fields):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="필수 항목 중 일부가 누락되었습니다")

    try:
        uid = token['uid']

        user = User(
            uid=uid,
            nickname=user_data['nickname'],
            created_at=datetime.now(),
            modified_at=datetime.now(),
            last_connection=datetime.now()
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "status_code": status.HTTP_201_CREATED,
            "detail": "사용자 생성 성공",
            "data": user
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="이미 존재하는 사용자입니다")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="사용자 생성 중 서버에 오류가 발생하였습니다")


# 사용자 조회를 위한 API
def get_user_by_id(db: Session, token: str):
    user = db.query(User).filter(User.uid == token['uid']).first()

    if user is not None:
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "사용자 조회 성공",
            "data": user
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="일치하는 사용자가 존재하지 않습니다")


# 사용자 업데이트를 위한 API
def update_user_by_id(data: dict, db: Session, token: str):
    user = get_user_by_id(db, token)['data']
    valid = False

    # 일치하는 항목이 사용자 모델에 존재하는지 체크
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
            valid = True
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="일치하는 항목이 존재하지 않습니다"
            )

    # 존재할 경우 업데이트 수행
    if valid is True:
        db.commit()
        db.refresh(user)

        return {
            "status_code": status.HTTP_200_OK,
            "detail": "사용자 업데이트 성공",
            "data": user
        }


# 사용자 삭제를 위한 API
def delete_user(db: Session, token: str):
    user = get_user_by_id(db, token)['data']

    db.delete(user)
    db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "사용자 삭제 성공",
    }
