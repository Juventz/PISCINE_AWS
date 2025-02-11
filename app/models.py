from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    age = Column(Integer)


class OperationsStats(Base):
    __tablename__ = 'operations_stats'
    operation_id = Column(String(255), primary_key=True, index=True)
    count = Column(Integer, nullable=False)
