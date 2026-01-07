#  Copyright (c) 2025 Ludovic Riffiod
#
from sqlalchemy import Column,  String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)
    events = relationship("Event", back_populates="client")
    votes = relationship("Vote", back_populates="user")