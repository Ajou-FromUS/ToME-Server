from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from db.session import Base
from db.models.user_model import User
from db.models.question_model import Question


class Archive(Base):
    __tablename__ = "archives"

    archive_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id),nullable=False)
    question_id = Column(Integer, ForeignKey(Question.question_id),nullable=False)
    user_answer = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)