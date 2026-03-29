#  Copyright (c) 2025 Ludovic Riffiod
#
import os

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
db_path : str | None = os.environ.get("SQLITE_DB_PATH")

if db_path is not None:
    engine = create_engine(
        db_path,
        connect_args={"check_same_thread": False},
        pool_size=5,
        max_overflow=0
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    yield db

