#  Copyright (c) 2025 Ludovic Riffiod
#
import random
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship, Session
from starlette import status

from .user import add_user_if_missing
from .base import Base, SessionLocal, engine
from .event import get_events
from .planet import get_planets
import uuid

from .. import model


def increase_vote(existing_event: model.ExistingEvent):
   with (SessionLocal() as session):
        result = engine.connect().execute(
            text("SELECT * FROM events WHERE client_id = :client_id and id = :event_id and planet_id = :planet_id"),
            {"event_id": existing_event.event_id, "client_id": existing_event.uuid, "planet_id": existing_event.planet_id},
        )

        exists = result.fetchall()

        client_uuid = existing_event.uuid

        if exists:
            return status.HTTP_403_FORBIDDEN, "You can't vote for your own event"

        exists = session.query(Vote.id).filter(
            (Vote.user_id == client_uuid) & Vote.event.has(planet_id=existing_event.planet_id)).first() is not None

        if exists:
            return status.HTTP_403_FORBIDDEN, "You already voted for an event today"

        try:
            add_user_if_missing(session, client_uuid)

            vote = Vote(
                user_id=client_uuid,
                event_id=existing_event.event_id,
            )

            session.add(vote)
            session.commit()
            return status.HTTP_200_OK, "Vote added"
        except Exception as e:
            print(e)
            return status.HTTP_403_FORBIDDEN,e

def fake_vote():
    today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_date_str = today_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    client_uuid = str(uuid.uuid4())
    planets = get_planets()

    for planet in planets:
        today_events = get_events( planet["id"], today_date_str)
        random_index =  random.randint(0, len(today_events)-1)
        random_event = today_events[random_index]
        existing_event: model.ExistingEvent = model.ExistingEvent(event_id=random_event["id"], uuid = client_uuid, planet_id=planet["id"])
        result = increase_vote(existing_event)
        print("fake vote for event: "+ random_event["title"]+" in planet : "+str(planet["id"])+" result : "+ str(result))

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)

    user_id = Column(String, ForeignKey("users.uuid"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="votes")
    event = relationship("Event", back_populates="votes")