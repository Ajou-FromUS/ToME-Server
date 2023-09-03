from fastapi import APIRouter

diary = APIRouter(
    prefix="/diary"
)


# 일기 조회를 위한 API
@diary.get('/')
async def get_diary():
    return {'msg': '일기 조회 성공'}


# 일기 생성을 위한 API
@diary.post('/')
async def create_diary():
    return {'msg': '일기 생성 성공'}


# 일기 업데이트를 위한 API
@diary.patch('/')
async def update_diary():
    return {'msg': '일기 업데이트 성공'}


# 일기 삭제를 위한 API
@diary.delete('/')
async def delete_diary():
    return {'msg': '일기 삭제 성공'}
