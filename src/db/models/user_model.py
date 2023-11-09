from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from db.session import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uid = Column(String(255), unique=True)
    nickname = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    last_connection = Column(DateTime, nullable=False)
