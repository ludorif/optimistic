#  Copyright (c) 2025 Ludovic Riffiod
#
import logging
import os

logger = logging.getLogger(__name__)

from fastapi import Depends
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from . import model
from .db import planet, event, vote, sql_model

SessionLocal : sessionmaker[Session]
database_url = os.environ.get("DATABASE_URL", "")
engine = create_engine(
    database_url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
)
sql_model.Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def post_planet(new_planet, session: Session):
    return planet.post_planet( new_planet, session)

def get_planets(session: Session):
    return planet.get_planets(session)

def get_summary(planet_id, session: Session):
    return planet.get_summary(planet_id, session)

def update_summary(planet_id, summary_content, session: Session):
    return planet.update_summary(planet_id, summary_content, session)


async def add_event_to_world(response_dict, client_uuid, planet_id, session: Session):
    await event.add_event_to_world( response_dict, client_uuid, planet_id, session)


def get_events(planet_id, date_str, session: Session):
   return event.get_events( planet_id, date_str, session)


def get_dates(planet_id, session: Session):
    return event.get_dates(planet_id, session)


def increase_vote(existing_event: model.ExistingEvent, session: Session):
   return vote.increase_vote( existing_event, session)


def get_winners(session: Session ):
    result = session.execute(text('SELECT * FROM events WHERE did_win = True'))
    events = result.mappings().all()
    return [dict(r) for r in events]

def define_all_winners(session: Session):
    return event.define_all_winners(session)



def get_health(session: Session):
    try:
        session.execute(text("SELECT 1"))
        logger.info("Database health check passed.")
    except Exception:
        logger.exception("Database health check failed")


def get_all_events_story(planet_id, session: Session):
    return get_events(planet_id, "", session)


async def add_new_event(new_event, response, session: Session):
    return await event.add_new_event( new_event, response, session)


async def create_fake_event(session: Session):
    return await event.create_fake_event(session)


def fake_vote(session: Session):
    vote.fake_vote(session)


