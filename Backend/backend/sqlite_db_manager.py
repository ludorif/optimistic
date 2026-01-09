#  Copyright (c) 2025 Ludovic Riffiod
#

from sqlalchemy import text

from . import model
from .db import planet, event, vote, base
from .db.base import engine


def create_all_tables():
    base.Base.metadata.create_all(engine)

def post_planet(new_planet):
    return planet.post_planet( new_planet)

def get_planets():
    return planet.get_planets()


async def add_event_to_world(response_dict, client_uuid, planet_id):
    await event.add_event_to_world( response_dict, client_uuid, planet_id)


def get_events(planet_id, date_str):
   return event.get_events( planet_id, date_str)


def get_dates(planet_id):
    return event.get_dates(planet_id)


def increase_vote(existing_event: model.ExistingEvent):
   return vote.increase_vote( existing_event)


def get_winners():
    result = engine.connect().execute(text('SELECT * FROM events WHERE did_win = True'))
    events = result.mappings().all()
    return [dict(r) for r in events]


def define_winner(today_date):
    planet_id_temp = 1
    today_events = get_events(planet_id_temp, today_date)


    if len(today_events) == 0:
        print("no events")
        return False


    winner = today_events[0]

    for today_event in today_events:
        if today_event["vote_count"] > winner["vote_count"]:
            winner = event

    print(winner["id"])

    with engine.begin() as conn:  # begin() automatically commits
        conn.execute(
            text("""
                UPDATE events
                SET did_win = TRUE
                WHERE id = :event_id
            """),
            {"event_id": winner["id"]}
        )

    return True


def get_health():
    """
        Check SQLite database health using SQLAlchemy.

        Args:
            db_url (str): SQLAlchemy database URL, e.g., "sqlite:///mydatabase.db"
            backup_path (str): Optional path to save a backup of the database
        """
    try:
        with engine.connect() as conn:
            # 1. Integrity check
            result = conn.execute(text("PRAGMA integrity_check;")).fetchone()
            if result[0] == "ok":
                print("✅ Integrity check passed.")
            else:
                print(f"❌ Integrity check failed: {result[0]}")

            # 2. Foreign key check
            fk_issues = conn.execute(text("PRAGMA foreign_key_check;")).fetchall()
            if not fk_issues:
                print("✅ Foreign key check passed.")
            else:
                print(f"❌ Foreign key issues found: {fk_issues}")
    except Exception as e:
        print(f"❌ Database error: {e}")


def get_all_events_story(planet_id):
    return get_events(planet_id, "")


async def add_new_event(new_event, response):
    return await event.add_new_event( new_event, response)


async def create_fake_event():
    return await event.create_fake_event()


def fake_vote():
    vote.fake_vote()