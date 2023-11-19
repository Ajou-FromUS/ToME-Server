from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uid = Column(String(255), unique=True)
    nickname = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    last_connection = Column(DateTime, nullable=False)

    user_missions = relationship("UserMission", back_populates="user")
