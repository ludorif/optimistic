#  Copyright (c) 2025 Ludovic Riffiod
#
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///optimistic_db.db")
SessionLocal = sessionmaker(bind=engine)