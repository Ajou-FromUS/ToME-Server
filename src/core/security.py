from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

import jwt
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY')


def verify_token(request: Request):
    try:
        # Header로부터 Access Token 추출
        access_token = request.headers['access_token']
        decoded_token = jwt.decode(access_token, secret_key, algorithms=["HS256"])

        return decoded_token
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            content={"status_code": status.HTTP_401_UNAUTHORIZED, "detail": "토큰이 만료되었습니다"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.DecodeError:
        return JSONResponse(
            content={"status_code": status.HTTP_401_UNAUTHORIZED, "detail": "올바르지 않은 토큰 형식입니다"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except BaseException:
        return JSONResponse(
            content={"status_code": status.HTTP_401_UNAUTHORIZED, "detail": "올바르지 않은 입력입니다"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
