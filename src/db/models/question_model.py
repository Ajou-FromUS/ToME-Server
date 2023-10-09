from sqlalchemy import Column, Integer, String, DateTime, Text
from db.session import Base


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)