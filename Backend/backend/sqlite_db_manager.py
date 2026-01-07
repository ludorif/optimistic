#  Copyright (c) 2025 Ludovic Riffiod
#
import os
from datetime import datetime, timezone, date

from sqlalchemy import create_engine, Column, Integer, String, text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from sqlalchemy.sql.sqltypes import Boolean
from starlette import status


Base = declarative_base()
engine = create_engine("sqlite:///optimistic_db.db")


def create_all_tables():
    Base.metadata.create_all(engine)


class Planet(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    first_story = Column(String)

    # one-to-many: Planet → Events
    events = relationship("Event", back_populates="planet")


class User(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)

    events = relationship("Event", back_populates="client")

    votes = relationship("Vote", back_populates="user")


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


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)

    user_id = Column(String, ForeignKey("users.uuid"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="votes")
    event = relationship("Event", back_populates="votes")



def post_planet(new_planet):
    with Session(engine) as session:
        sql_planet = Planet(name=new_planet.name, type =new_planet.type,  first_story=new_planet.first_story)
        session.add(sql_planet)
        session.commit()
        return sql_planet.id



def get_planets():
    result = engine.connect().execute(text('SELECT * FROM planets'))
    planets = result.mappings().all()
    return [dict(row) for row in planets]


async def add_event_to_world(response_dict, client_uuid, planet_id):
    try:
        with Session(engine) as session:
            result = engine.connect().execute(
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


def get_events(planet_id, date_str):
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


def get_dates():
    result = engine.connect().execute(text('SELECT DISTINCT created_at FROM events'))
    events = result.mappings().all()
    return [dict(r) for r in events]


def increase_vote(event_id, client_uuid):
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


def check_current_events(event_date, uuid):
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

    for event in today_events:
        if len(event["votes"]) > len(winner["votes"]):
            winner = event

    engine.connect().execute(text("""
        UPDATE events 
        set did_win = True 
        where id = :event_id   
        """),
{"event_id": winner["id"]})

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