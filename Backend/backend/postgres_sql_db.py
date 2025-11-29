#  Copyright (c) 2025 Ludovic Riffiod
#
import os

from sqlalchemy import create_engine, Column, Integer, String, text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql.sqltypes import Boolean

engine = create_engine(os.environ["POSTGRES_DB_URI"])
Base = declarative_base()


class Planet(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    summary = Column(String)

    # one-to-many: Planet → Memories
    memories = relationship("Memory", back_populates="planet")



class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True)
    story = Column(String)
    created_at = Column(DateTime(timezone=True))
    did_win = Column(Boolean, default=False, nullable=False)

    # Foreign key to Planet
    planet_id = Column(Integer, ForeignKey("planets.id"), nullable=False)

    # relationship back to Planet
    planet = relationship("Planet", back_populates="memories")




def test():
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    mars = Planet(name="Mars", summary="Red planet")
    session.add(mars)
    session.commit()

    memory = Memory(
        story="First landing!",
        did_win=False,
        planet_id=mars.id
    )

    session.add(memory)
    session.commit()

    result = engine.connect().execute(text('SELECT story FROM memories'))
    names = [row[0] for row in result]
    print(names)
