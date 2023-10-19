from fastapi import FastAPI
from config.database import Base
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime


class Users(Base):
    """
    Table used for stored the users information
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(String(100), nullable=False, unique=True, doc='unique_id')
    first_name = Column(String(255), doc='First name of user', nullable=True)
    last_name = Column(String(255), doc='Last name of user', nullable=True)
    email = Column(String(100), doc='Email ID of the user', nullable=True)
    username = Column(String(100), doc='Username of the user', nullable=True)
    password = Column(String(100), doc='Password of the user', nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, 
                        doc='its generate automatically when data create')
    updated_at = Column(DateTime, nullable=True,
                        onupdate=datetime.utcnow, doc='its generate automatically when data update')
    deleted_at = Column(DateTime, nullable=True,
                        doc='its generate automatically when data deleted')