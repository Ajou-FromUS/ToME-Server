from fastapi import HTTPException, status, Request
from dotenv import load_dotenv

import jwt
import os
import requests

load_dotenv()

secret_key = os.getenv('SECRET_KEY')


def verify_token(request: Request):
    try:
        # Header로부터 Access Token 추출
        access_token = request.headers['access_token']
        refresh_token = request.headers['refresh_token']

        # 추출된 Access Token 검증
        decoded_token = jwt.decode(access_token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 만료되었습니다")

        # Access Token이 만료됐을 경우 Refresh Token을 통해 재발급
        url = 'https://api.furo.one/sessions/token/refresh'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {refresh_token}'
        }
        data = {'accessToken': access_token}
        response = requests.post(url, headers=headers, json=data)
        print(response.json())

    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Input")
