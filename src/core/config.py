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


settings = Settings()
