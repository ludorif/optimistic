#  Copyright (c) 2025 Ludovic Riffiod
#
from sqlalchemy import text, select
from sqlalchemy.orm import  Session

from backend.db.sql_model import Planet


def post_planet(new_planet, session: Session ):
    sql_planet = Planet(name=new_planet.name, type =new_planet.type)
    session.add(sql_planet)
    session.commit()
    return sql_planet.id


def get_planets(session: Session ):
    result = session.execute(text('SELECT * FROM planets'))
    planets = result.mappings().all()
    return [dict(row) for row in planets]


def update_summary(planet_id, summary_content, session):
    result = session.execute(
        text("""
                UPDATE planets
                SET summary = :summary_content
                WHERE id = :planet_id
            """),
        {"summary_content": summary_content, "planet_id": planet_id}
    )
    session.commit()


def get_summary(planet_id: int, session):
    result = session.execute(
        select(Planet.summary).where(Planet.id == planet_id)
    )

    return result.scalar_one_or_none()