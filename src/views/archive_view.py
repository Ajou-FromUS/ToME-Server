# from sqlalchemy.orm import Session, joinedload
# from sqlalchemy.exc import IntegrityError
# from fastapi import HTTPException, status
# from datetime import datetime
# from db.models.archive_model import Archive
# from db.models.question_model import Question

# import traceback

# # 아카이브 저장을 위한 API
# def create_archive(archive_data: dict, db: Session):
#     # 필수 항목 누락 체크
#     required_fields = ['user_id', 'question_id', 'question_text', 'user_answer']
#     if not all(field in archive_data for field in required_fields):
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                             detail="필수 항목 중 일부가 누락되었습니다")

#     try:
#         archive = Archive(
#             user_id=archive_data['user_id'],
#             question_id = archive_data['question_id'],
#             user_answer=archive_data['user_answer'],
#             created_at=datetime.now()
#         )

#         db.add(archive)
#         db.commit()
#         db.refresh(archive)

#         return {
#             "status_code": status.HTTP_201_CREATED,
#             "detail": "아카이브 저장 성공",
#             "data": archive
#         }
#     except Exception:
#         db.rollback()
#         traceback.print_exc() 
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="아카이브 저장 중 서버에 오류가 발생하였습니다")


# # 아카이브 조회를 위한 API
# def get_archive_by_id(user_id: int, archive_id:int, db: Session):
#     archives = db.query(Archive).filter(Archive.user_id == user_id, Archive.archive_id ==archive_id).all()
#     archives = sorted(archives, key=lambda d: d.archive_id)
#     temp_archive = archives[0]
#     question = db.query(Question).filter(Question.question_id==temp_archive.question_id).first()
#     question_text=question.question_text
#     if archives is not None:
#         return {
#             "status_code": status.HTTP_200_OK,
#             "detail": "아카이브 조회 성공",
#             "question_text":question_text,
#             "data": archives
#         }
#     else:
#         traceback.print_exc()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="아카이브 조회에 실패하였습니다")


# # # 사용자 업데이트를 위한 API
# # def update_user_by_id(user_id: int, data: dict, db: Session):
# #     user = get_user_by_id(user_id, db)['data']
# #     valid = False

# #     # 일치하는 항목이 사용자 모델에 존재하는지 체크
# #     for key, value in data.items():
# #         if hasattr(user, key):
# #             setattr(user, key, value)
# #             valid = True
# #         else:
# #             raise HTTPException(
# #                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
# #                 detail="일치하는 항목이 존재하지 않습니다"
# #             )

# #     # 존재할 경우 업데이트 수행
# #     if valid is True:
# #         db.commit()
# #         db.refresh(user)

# #         return {
# #             "status_code": status.HTTP_200_OK,
# #             "detail": "사용자 업데이트 성공",
# #             "data": user
# #         }


# # # 사용자 삭제를 위한 API
# # def delete_user(user_id: int, db: Session):
# #     user = get_user_by_id(user_id, db)['data']

# #     db.delete(user)
# #     db.commit()

# #     return {
# #         "status_code": status.HTTP_200_OK,
# #         "detail": "사용자 삭제 성공",
# #     }
