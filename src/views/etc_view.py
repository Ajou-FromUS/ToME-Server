from PIL import Image
from io import BytesIO
from fastapi import Request
# from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions

import numpy as np
import requests

# ImageNet으로 미리 훈련된 InceptionV3 모델 로드
# model = InceptionV3(weights='imagenet')


def refresh_token(request):
    access_token = request.headers['access_token']
    refresh_token = request.headers['refresh_token']

    url = 'https://api.furo.one/sessions/token/refresh'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {refresh_token}'
    }
    data = {'accessToken': access_token}
    response = requests.post(url, headers=headers, json=data)

    new_token = response.json().get('access_token')
    return {'access_token': new_token} if new_token else None


# 이미지 분류 함수 정의
# def classify_image_by_imagenet(image):
#     img = Image.open(BytesIO(image))
#     img = img.resize((299, 299))
#     img = np.array(img)
#     img = np.expand_dims(img, axis=0)
#     img = preprocess_input(img)

#     predictions = model.predict(img)
#     decoded_predictions = decode_predictions(predictions, top=3)[0]

#     results = [{"label": label, "description": description, "probability": probability} for (label, description, probability) in decoded_predictions]
#     return results
