#  Copyright (c) 2025 Ludovic Riffiod
#
import random
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import  Session
from starlette import status

from .sql_model import Vote
from .user import add_user_if_missing
from .event import get_events
from .planet import get_planets
import uuid

from .. import model


def increase_vote(existing_event: model.ExistingEvent, session: Session ):
    result = session.execute(
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
        add_user_if_missing(client_uuid, session)

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

def fake_vote(session: Session):
    today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_date_str = today_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    client_uuid = str(uuid.uuid4())
    planets = get_planets(session)

    for planet in planets:
        today_events = get_events( planet["id"], today_date_str, session)
        random_index =  random.randint(0, len(today_events)-1)
        random_event = today_events[random_index]
        existing_event: model.ExistingEvent = model.ExistingEvent(event_id=random_event["id"], uuid = client_uuid, planet_id=planet["id"])
        result = increase_vote(existing_event, session)
        print("fake vote for event: "+ random_event["title"]+" in planet : "+str(planet["id"])+" result : "+ str(result))

