from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base


class UserMission(Base):
    __tablename__ = "userMissions"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.id'), nullable=False)
    mission_id = Column(Integer, ForeignKey('missions.id'), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="user_missions")
    mission = relationship("Mission", back_populates="user_missions")
