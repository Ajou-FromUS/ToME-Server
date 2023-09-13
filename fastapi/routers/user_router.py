from fastapi import APIRouter, Depends

user = APIRouter(
    prefix="/user"
)


# 사용자 조회를 위한 API
@user.get('/')
async def get_user():
    return {'msg': '사용자 조회 성공'}


# 사용자 생성을 위한 API
@user.post('/')
async def create_user():
    return {'msg': '사용자 생성 성공'}


# 사용자 업데이트를 위한 API
@user.patch('/')
async def update_user():
    return {'msg': '사용자 업데이트 성공'}


# 사용자 삭제를 위한 API
@user.delete('/')
async def delete_user():
    return {'msg': '사용자 삭제 성공'}
