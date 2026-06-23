
import os
from re import S
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.core.config import settings


print("database url...",settings.DATABASE_URL)

engine=create_engine(settings.DATABASE_URL,
                     echo=False,
                     )

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()