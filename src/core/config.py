import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_DATABASE: str = os.getenv("DB_DATABASE")

    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

    SECRET_KEY = os.getenv("CLIENT_SECRET")

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")

    CHAT_LOG_PATH: str = os.getenv("CHAT_LOG_PATH")
    CHAT_INPUT_TEXT: str = os.getenv("CHAT_INPUT_TEXT")

    CLOVA_BASE_URL: str = os.getenv("CLOVA_BASE_URL")
    CLOVA_API_KEY_ID: str = os.getenv("CLOVA_API_KEY_ID")
    CLOVA_API_KEY: str = os.getenv("CLOVA_API_KEY")

    KEYWORD_IMG_PATH: str = os.getenv("KEYWORD_IMG_PATH")

    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY")
    S3_REGION: str = os.getenv("S3_REGION")
    S3_BUCKET_URL: str = os.getenv("S3_BUCKET_URL")

    LOG_PATH: str = os.getenv("LOG_PATH")

settings = Settings()
