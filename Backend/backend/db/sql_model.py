from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, text, DateTime, Boolean
from sqlalchemy.orm import relationship, Session, DeclarativeBase

class Base(DeclarativeBase):
    pass

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

class Planet(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    summary = Column(String)

    # one-to-many: Planet → Events
    events = relationship("Event", back_populates="planet")

class User(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True)
    events = relationship("Event", back_populates="client")
    votes = relationship("Vote", back_populates="user")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)

    user_id = Column(String, ForeignKey("users.uuid"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="votes")
    event = relationship("Event", back_populates="votes")

