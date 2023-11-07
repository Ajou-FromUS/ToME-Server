from sqlalchemy import Column, Integer, String, DateTime
from db.session import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(255), nullable=False)
    milestone = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    last_connection = Column(DateTime, nullable=False)
