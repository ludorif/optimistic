#  Copyright (c) 2025 Ludovic Riffiod
#
import logging
import uuid

logger = logging.getLogger(__name__)

from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, text, func
from sqlalchemy.orm import relationship, Session
from starlette import status

from .planet import get_planets
from .sql_model import Event
from .user import add_user_if_missing
from datetime import datetime, timezone

from .. import model, gemini_ai_manager
from starlette.responses import Response

from ..model import NewEvent, ExistingEvent


async def add_new_event(new_event: model.NewEvent, response: Response, session: Session):
    number_of_events, user_already_participated = check_current_events( new_event.event_date, new_event.uuid, new_event.planet_id, session)

    logger.info("number_of_events %s", number_of_events)

    if user_already_participated:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Already participated"}
    elif number_of_events >= 3:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Enough events for today"}
    else:
        await add_new_event_internal( new_event, session)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "New event added"}

async def add_new_event_internal( new_event: model.NewEvent, session: Session):
    response_dict = gemini_ai_manager.generate_new_event(new_event.story)
    await add_event_to_world( response_dict, new_event.uuid, new_event.planet_id, session)


async def add_event_to_world( response_dict, client_uuid, planet_id, session: Session ):
    try:
        add_user_if_missing( client_uuid, session)

        created_at_converted = datetime.strptime(
            response_dict["date"],
            "%Y-%m-%d"
        ).replace(tzinfo=timezone.utc)

        event = Event(
            title=response_dict["title"],
            content=response_dict["content"],
            created_at=created_at_converted,
            photoId=response_dict["photoId"],
            client_id=client_uuid,
            did_win=False,
            planet_id=planet_id
        )

        session.add(event)
        session.commit()
    except Exception as e:
        logger.exception("Failed to add event to world")

def get_dates(planet_id, session: Session ):
    query = """
            SELECT DISTINCT created_at
            FROM events 
            WHERE planet_id = :planet_id
        """

    params = {"planet_id": planet_id}
    result = session.execute(text(query), params)
    events = result.mappings().all()
    return [dict(r) for r in events]

def get_events( planet_id, date_str, session: Session ):
    query = """
        SELECT
            e.*,
            COUNT(v.id) AS vote_count
        FROM events e
        LEFT JOIN votes v ON v.event_id = e.id
        WHERE planet_id = :planet_id
    """

    params = {"planet_id": planet_id}


    if date_str:
        iso_date = datetime.fromisoformat(
            date_str.replace("Z", "+00:00")
        ).date()

        query += " AND DATE(e.created_at) = DATE(:date)"
        params["date"] = iso_date

    query += """ 
        GROUP BY e.id
        ORDER BY created_at;"""

    #session.get(ExistingEvent, params)
    result = session.execute(text(query), params)

    events = result.mappings().all()
    return [dict(r) for r in events]


def define_all_winners(session: Session):
    today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_date_str = today_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    planets = get_planets( session)
    for planet in planets:
        define_winner( today_date_str, planet["id"], session)


def define_winner(today_date_str, planet_id, session: Session):
    today_events = get_events(planet_id, today_date_str, session)

    if len(today_events) == 0:
        logger.info("no events for planet %s", planet_id)
        return False

    winner = today_events[0]

    for today_event in today_events:
        if today_event["vote_count"] > winner["vote_count"]:
            winner = today_event

    logger.info("winner is %s for planet %s", winner["title"], planet_id)

    session.execute(
        text("""
            UPDATE events
            SET did_win = TRUE
            WHERE id = :event_id
        """),
        {"event_id": winner["id"]}
    )
    session.commit()

    return True

def check_current_events( event_date : str, client_uuid, planet_id,session: Session ):
    dic_results = get_events( planet_id, event_date, session)
    number_of_events = len( dic_results)
    user_already_participated: bool = False

    for event in dic_results:
        if event["client_id"] == client_uuid:
            user_already_participated = True
            break

    return number_of_events, user_already_participated

async def create_fake_event(session: Session):
    today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_date_str = today_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    planets = get_planets(session)

    for planet in planets:
        fake_new_event: model.NewEvent = NewEvent(story="", event_date= today_date_str, uuid=str(uuid.uuid4()), planet_id=planet["id"])
        response: Response = Response()
        await add_new_event( fake_new_event, response, session)
        logger.info("created fake event for planet: %s status code: %s", planet["name"], response.status_code)





