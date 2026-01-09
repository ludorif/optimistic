#  Copyright (c) 2025 Ludovic Riffiod
#
from sqlalchemy import Column, String, text
from sqlalchemy.orm import relationship
from .base import Base, SessionLocal


def add_user_if_missing( client_uuid):
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT * FROM users WHERE uuid = :client_id "),
            {"client_id": client_uuid}  # safe binding
        )

        exists = result.fetchall()

        if not exists:
            user = User(
                uuid=client_uuid
            )
            session.add(user)
            session.commit()

class User(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)
    events = relationship("Event", back_populates="client")
    votes = relationship("Vote", back_populates="user")