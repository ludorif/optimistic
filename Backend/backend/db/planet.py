#  Copyright (c) 2025 Ludovic Riffiod
#
from sqlalchemy import  text
from sqlalchemy.orm import  Session

from backend.db.sql_model import Planet


def post_planet(new_planet, session: Session ):
    sql_planet = Planet(name=new_planet.name, type =new_planet.type,  first_story=new_planet.first_story)
    session.add(sql_planet)
    session.commit()
    return sql_planet.id


def get_planets(session: Session ):
    result = session.execute(text('SELECT * FROM planets'))
    planets = result.mappings().all()
    return [dict(row) for row in planets]


