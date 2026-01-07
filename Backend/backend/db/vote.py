#  Copyright (c) 2025 Ludovic Riffiod
#

from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship, Session
from starlette import status

from .user import User
from .base import Base

def increase_vote(engine, event_id, client_uuid):
    with Session(engine) as session:
        result = engine.connect().execute(
            text("SELECT * FROM events WHERE client_id = :client_id and id = :event_id"),
            {"event_id": event_id,
                      "client_id": client_uuid}  # safe binding
        )

        exists = result.fetchall()

        if exists:
            return status.HTTP_403_FORBIDDEN, "You can't vote for your own event"

        exists = session.query(Vote.id).filter(Vote.user_id == client_uuid).first() is not None
        if exists:
            return status.HTTP_403_FORBIDDEN, "You already voted for this event"

        try:
            user = User(
                uuid=client_uuid
            )
            session.add(user)
            session.commit()

            vote = Vote(
                user_id=client_uuid,
                event_id=event_id,
            )

            session.add(vote)
            session.commit()
            return status.HTTP_200_OK, "Vote added"
        except Exception as e:
            print(e)
            return status.HTTP_403_FORBIDDEN,e


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)

    user_id = Column(String, ForeignKey("users.uuid"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="votes")
    event = relationship("Event", back_populates="votes")