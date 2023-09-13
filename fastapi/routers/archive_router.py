from fastapi import APIRouter

archive = APIRouter(
    prefix="/archive"
)


# 아카이브 조회를 위한 API
@archive.get('/')
async def get_archive():
    return {'msg': '아카이브 조회 성공'}


# 아카이브 생성을 위한 API
@archive.post('/')
async def create_archive():
    return {'msg': '아카이브 생성 성공'}


# 아카이브 업데이트를 위한 API
@archive.patch('/')
async def update_archive():
    return {'msg': '아카이브 업데이트 성공'}


# 아카이브 삭제를 위한 API
@archive.delete('/')
async def delete_archive():
    return {'msg': '아카이브 삭제 성공'}

