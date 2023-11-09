from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db.session import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=True)
    type = Column(Integer, nullable=False)
    emotion = Column(Integer, nullable=False)
