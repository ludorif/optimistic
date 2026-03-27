#  Copyright (c) 2025 Ludovic Riffiod
#
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import model
from .db import planet, event, vote, base
from .db.base import engine, SessionLocal, get_db


def create_all_tables():
    base.Base.metadata.create_all(engine)

def post_planet(new_planet, session: Session):
    return planet.post_planet( new_planet, session)

def get_planets(session: Session):
    return planet.get_planets(session)


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

def define_all_winners():
    return event.define_all_winners()



def get_health(session: Session ):
    """
        Check SQLite database health using SQLAlchemy.

        Args:
            db_url (str): SQLAlchemy database URL, e.g., "sqlite:///mydatabase.db"
            backup_path (str): Optional path to save a backup of the database
        """
    try:
        # 1. Integrity check
        result = session.execute(text("PRAGMA integrity_check;")).fetchone()
        if result[0] == "ok":
            print("✅ Integrity check passed.")
        else:
            print(f"❌ Integrity check failed: {result[0]}")

        # 2. Foreign key check
        fk_issues = session.execute(text("PRAGMA foreign_key_check;")).fetchall()
        if not fk_issues:
            print("✅ Foreign key check passed.")
        else:
            print(f"❌ Foreign key issues found: {fk_issues}")
    except Exception as e:
        print(f"❌ Database error: {e}")


def get_all_events_story(planet_id, session: Session):
    return get_events(planet_id, "", session)


async def add_new_event(new_event, response, session: Session):
    return await event.add_new_event( new_event, response, session)


async def create_fake_event(session: Session):
    return await event.create_fake_event(session)


def fake_vote(session: Session):
    vote.fake_vote(session)