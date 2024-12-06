"""This config file will define Database Url and configurations"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import env_config

# ##### DATABASE CONFIGURATION ############################
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{env_config.DATABASE_USER}:{env_config.DATABASE_PASSWORD}@{env_config.DATABASE_HOST}:{env_config.DATABASE_PORT}/{env_config.DATABASE_NAME}'

# Create engine by sqlalchemy db url
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    """This function returns the database object."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
