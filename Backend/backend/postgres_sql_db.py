#  Copyright (c) 2025 Ludovic Riffiod
#
import json
import os
from datetime import datetime, timezone

from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String, text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from sqlalchemy.sql.sqltypes import Boolean
from starlette import status


Base = declarative_base()
engine = create_engine(os.environ["POSTGRES_DB_URI"])


def create_all_tables():
    Base.metadata.create_all(engine)


class Planet(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    first_story = Column(String)

    # one-to-many: Planet → Memories
    memories = relationship("Memory", back_populates="planet")


class User(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)

    # memories created by the user
    memories = relationship("Memory", back_populates="client")

    # votes cast by the user
    votes = relationship("Vote", back_populates="user")


class Memory(Base):
    __tablename__ = "memories"
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
    planet = relationship("Planet", back_populates="memories")
    client = relationship("User", back_populates="memories")
    votes = relationship("Vote", back_populates="memory", cascade="all, delete-orphan")


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)

    user_id = Column(String, ForeignKey("users.uuid"), nullable=False)
    memory_id = Column(Integer, ForeignKey("memories.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="votes")
    memory = relationship("Memory", back_populates="votes")



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

            memory = Memory(
                title=response_dict["title"],
                content=response_dict["content"],
                created_at=response_dict["date"],
                photoId=response_dict["photoId"],
                client_id=client_uuid,
                did_win=False,
                planet_id=planet_id
            )

            session.add(memory)
            session.commit()
    except Exception as e:
        print(e)


def get_events(planet_id, date):
    query = """
        SELECT
            m.*,
            COUNT(v.id) AS vote_count
        FROM memories m
        LEFT JOIN votes v ON v.memory_id = m.id
        WHERE planet_id = :planet_id
    """

    params = {"planet_id": planet_id}

    if date:
        query += " AND DATE(m.created_at) = DATE(:date)"
        params["date"] = date

    query += """ 
        GROUP BY m.id
        ORDER BY created_at;"""

    result = engine.connect().execute(text(query), params)

    memories = result.mappings().all()
    return [dict(r) for r in memories]


def get_dates():
    result = engine.connect().execute(text('SELECT created_at FROM memories'))
    memories = result.mappings().all()
    return [dict(r) for r in memories]


def increase_vote(event_id, client_uuid):
    with Session(engine) as session:
        result = engine.connect().execute(
            text("SELECT * FROM memories WHERE client_id = :client_id and id = :event_id"),
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
                memory_id=event_id,
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
            FROM memories m    
            WHERE m.created_at = :date
            """),
    {"date": event_date})

        number_of_events = len( result.mappings().all())
        user_already_participated = session.query(Memory.id).filter((Memory.client_id == uuid) & (Memory.created_at == event_date)).first() is not None
        return number_of_events, user_already_participated


def get_winners():
    result = engine.connect().execute(text('SELECT * FROM memories WHERE did_win = True'))
    memories = result.mappings().all()
    return [dict(r) for r in memories]