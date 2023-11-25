from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=True)
    type = Column(Integer, nullable=False)
    emotion = Column(Integer, nullable=False)
    keyword = Column(String(255), nullable=True)

    user_missions = relationship("UserMission", back_populates="mission")
