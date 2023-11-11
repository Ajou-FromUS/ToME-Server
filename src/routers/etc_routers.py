from fastapi import APIRouter, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from views import etc_view

etc = APIRouter()


# 애플리케이션 로딩시 필요 데이터를 조회하기 위한 API
@etc.get('/', response_class=HTMLResponse)
async def init_client(request: Request):
    return {'msg': '~~~~'}


# 챗봇으로부터 응답을 받기 위한 API
@etc.get('/get-response')
async def get_chatbot_response():
    return {'msg': '~~~~'}


# 사용자의 월간 활동기록을 조회하기 위한 API
@etc.get('/get-monthly-log')
async def get_monthly_log():
    return {'msg': '~~~'}


# 사용자의 Toekn을 재발급하기 위한 API
@etc.get('/refresh-token')
async def refresh_user_token(request: Request):
    return etc_view.refresh_token(request)


# 이미지 디텍션을 위한 API
# @etc.post('/classify')
# async def classify_image(file: UploadFile):
#     image = await file.read()
#     etc_view.classify_image_by_imagenet(image)
