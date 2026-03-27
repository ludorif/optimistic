#  Copyright (c) 2025 Ludovic Riffiod
#
import os

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine(
    os.environ["SQLITE_DB_PATH"],
    connect_args={"check_same_thread": False},
    pool_size=5,
    max_overflow=0
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    yield db