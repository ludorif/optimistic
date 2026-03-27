#  Copyright (c) 2025 Ludovic Riffiod
#
from fastapi import Depends
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import relationship, Session
from .base import Base, SessionLocal, get_db


def post_planet(new_planet, session: Session ):
    sql_planet = Planet(name=new_planet.name, type =new_planet.type,  first_story=new_planet.first_story)
    session.add(sql_planet)
    session.commit()
    return sql_planet.id


def get_planets(session: Session ):
    result = session.execute(text('SELECT * FROM planets'))
    planets = result.mappings().all()
    return [dict(row) for row in planets]


class Planet(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    first_story = Column(String)

    # one-to-many: Planet → Events
    events = relationship("Event", back_populates="planet")