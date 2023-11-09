from fastapi import HTTPException, status, Request
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 만료되었습니다")
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except BaseException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Input")
