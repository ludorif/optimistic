#  Copyright (c) 2025 Ludovic Riffiod
#
import uuid

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship, Session
from starlette import status

from .planet import get_planets
from .user import add_user_if_missing
from .base import Base, SessionLocal, engine
from datetime import datetime, timezone

from .. import model, gemini_ai_manager
from starlette.responses import Response

from ..model import NewEvent


async def add_new_event(new_event: model.NewEvent, response: Response):
    number_of_events, user_already_participated = check_current_events( new_event.event_date, new_event.uuid, new_event.planet_id)

    print("number_of_events ", number_of_events)

    if user_already_participated:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Already participated"}
    elif number_of_events >= 3:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Enough events for today"}
    else:
        await add_new_event_internal( new_event)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "New event added"}

async def add_new_event_internal( new_event: model.NewEvent):
    response_dict = gemini_ai_manager.generate_new_event(new_event.story)
    await add_event_to_world( response_dict, new_event.uuid, new_event.planet_id)


async def add_event_to_world( response_dict, client_uuid, planet_id):
    try:
       with SessionLocal() as session:
            add_user_if_missing( client_uuid)

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
        print(e)

def get_dates(planet_id):
    with SessionLocal() as session:
        query = """
                SELECT DISTINCT created_at
                FROM events 
                WHERE planet_id = :planet_id
            """

        params = {"planet_id": planet_id}
        result = session.execute(text(query), params)
        events = result.mappings().all()
        return [dict(r) for r in events]

def get_events( planet_id, date_str):
    with SessionLocal() as session:
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


        result = session.execute(text(query), params)

        events = result.mappings().all()
        return [dict(r) for r in events]


def check_current_events( event_date, client_uuid, planet_id):
   with SessionLocal() as session:
        dic_results = get_events( planet_id, event_date)
        number_of_events = len( dic_results)
        user_already_participated = session.query(Event.id).filter((Event.client_id == client_uuid) & (Event.created_at == event_date)).first() is not None
        return number_of_events, user_already_participated

async def create_fake_event():
    today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_date_str = today_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    planets = get_planets()

    for planet in planets:
        fake_new_event: model.NewEvent = NewEvent(story="", event_date= today_date_str, uuid=str(uuid.uuid4()), planet_id=planet["id"])
        response: Response = Response()
        await add_new_event( fake_new_event, response)
        print("created fake event for planet: "+ planet["name"]+" status code : "+ str(response.status_code))


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    photoId = Column(String)
    did_win = Column(Boolean, default=False, nullable=False)

    # Foreign keys
    planet_id = Column(Integer, ForeignKey("planets.id"), nullable=False)
    client_id = Column(String, ForeignKey("users.uuid"), nullable=False)

    # Relationships
    planet = relationship("Planet", back_populates="events")
    client = relationship("User", back_populates="events")
    votes = relationship("Vote", back_populates="event", cascade="all, delete-orphan")


