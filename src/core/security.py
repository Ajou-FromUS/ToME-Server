from fastapi import HTTPException, status, Request
from dotenv import load_dotenv

import jwt
import os
import logging

load_dotenv()

secret_key = os.getenv('SECRET_KEY')

logger=logging.getLogger()

def verify_token(request: Request):
    try:
        # Header로부터 Access Token 추출
        access_token = request.headers['access_token']
        decoded_token = jwt.decode(access_token, secret_key, algorithms=["HS256"])

        return decoded_token
    except jwt.ExpiredSignatureError:
        logger.error(f"Access Token Expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다"
        )
    except jwt.DecodeError:
        logger.error(f"Access Token Decoding Error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="올바르지 않은 토큰 형식입니다"
        )
    except BaseException:
        logger.error(f"Access Token Is Invalid")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="올바르지 않은 입력입니다"
        )
