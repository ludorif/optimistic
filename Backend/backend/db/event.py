#  Copyright (c) 2025 Ludovic Riffiod
#
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship, Session
from starlette import status

from .user import add_user_if_missing
from .base import Base
from datetime import datetime, timezone

from .. import model, gemini_ai_manager
from starlette.responses import Response


async def add_event_to_world(engine, response_dict, client_uuid, planet_id):
    try:
        with Session(engine) as session:
            add_user_if_missing(engine, session, client_uuid)

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


def get_events(engine, planet_id, date_str):
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


    result = engine.connect().execute(text(query), params)

    events = result.mappings().all()
    return [dict(r) for r in events]


def get_dates(engine):
    result = engine.connect().execute(text('SELECT DISTINCT created_at FROM events'))
    events = result.mappings().all()
    return [dict(r) for r in events]


def check_current_events(engine, event_date, uuid):
    with Session(engine) as session:
        result = engine.connect().execute(text("""
            SELECT *
            FROM events e    
            WHERE e.created_at = :date
            """),
    {"date": event_date})

        number_of_events = len( result.mappings().all())
        user_already_participated = session.query(Event.id).filter((Event.client_id == uuid) & (Event.created_at == event_date)).first() is not None
        return number_of_events, user_already_participated

async def add_new_event(engine, new_event: model.NewEvent, response: Response):
    number_of_events, user_already_participated = check_current_events(engine, new_event.event_date, new_event.uuid)

    print("number_of_events ", number_of_events)

    if user_already_participated:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Already participated"}
    elif number_of_events >= 3:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Enough events for today"}
    else:
        await add_new_event_internal(engine, new_event)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "New event added"}

async def add_new_event_internal(engine, new_event: model.NewEvent):
    response_dict = gemini_ai_manager.generate_new_event(new_event.story)
    await add_event_to_world(engine, response_dict, new_event.uuid, new_event.planet_id)

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