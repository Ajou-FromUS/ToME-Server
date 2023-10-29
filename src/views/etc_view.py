from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions

# ImageNet으로 미리 훈련된 InceptionV3 모델 로드
model = InceptionV3(weights='imagenet')


# 이미지 분류 함수 정의
def classify_image_by_imagenet(image):
    img = Image.open(BytesIO(image))
    img = img.resize((299, 299))
    img = np.array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    predictions = model.predict(img)
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    results = [{"label": label, "description": description, "probability": probability} for (label, description, probability) in decoded_predictions]
    return results
