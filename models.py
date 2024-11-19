from sqlalchemy import (
    Float, Column, ForeignKey, Integer, String, Date
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import date


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

    activities = relationship('DailyActivity', back_populates='user')


class DailyActivity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, index=True)
    steps_taken = Column(Integer)
    calories_burned = Column(Float)
    water_intake = Column(Float)
    sleep_hours = Column(Float)
    date = Column(Date, default=date.today(), index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='activities')
