from sqlalchemy import Column, Integer, String, DateTime
from db.session import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(255), nullable=False)
    milestone = Column(Integer, nullable=False)
    current_character_id = Column(Integer, nullable=False)
    current_character_exp = Column(Integer, nullable=False)
    snack_num = Column(Integer, nullable=False)
    access_token = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    last_connection = Column(DateTime, nullable=False)
