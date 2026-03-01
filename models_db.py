from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    lang = Column(String)
    salary = Column(Integer)
    active = Column(Boolean, default=True)
    level = Column(String, default="middle")

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

