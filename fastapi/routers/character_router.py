from fastapi import APIRouter

character = APIRouter(
    prefix="/character"
)


# 캐릭터 조회를 위한 API
@character.get('/')
async def get_character():
    return {'msg': '캐릭터 조회 성공'}


# 캐릭터 생성을 위한 API
@character.post('/')
async def create_character():
    return {'msg': '캐릭터 생성 성공'}


# 캐릭터 업데이트를 위한 API
@character.patch('/')
async def update_character():
    return {'msg': '캐릭터 업데이트 성공'}


# 캐릭터 삭제를 위한 API
@character.delete('/')
async def delete_character():
    return {'msg': '캐릭터 삭제 성공'}

