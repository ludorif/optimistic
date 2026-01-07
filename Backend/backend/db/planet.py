#  Copyright (c) 2025 Ludovic Riffiod
#
from boto3 import Session
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import relationship
from .base import Base


class Planet(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    first_story = Column(String)

    # one-to-many: Planet → Events
    events = relationship("Event", back_populates="planet")


def post_planet(engine, new_planet):
    with Session(engine) as session:
        sql_planet = Planet(name=new_planet.name, type =new_planet.type,  first_story=new_planet.first_story)
        session.add(sql_planet)
        session.commit()
        return sql_planet.id



def get_planets(engine):
    result = engine.connect().execute(text('SELECT * FROM planets'))
    planets = result.mappings().all()
    return [dict(row) for row in planets]