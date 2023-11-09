from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.session import engine
from db.models.user_model import User
from db.models.mission_model import Mission

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class UserMission(Base):
    __tablename__ = "userMissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    mission_id = Column(Integer, ForeignKey(Mission.id), nullable=False)
    content = Column(String(255), nullable=True)
    is_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_missions")
    mission = relationship("Mission", back_populates="user_missions")
