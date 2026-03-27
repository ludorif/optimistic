import json
import uuid
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.base import get_db, Base
from backend.main import app
from backend.model import NewEvent

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()

    Base.metadata.create_all(bind=connection)

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()  # 🔥 wipes all changes
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()







def test_events(client):
    response = client.get("/events/?planet_id=1")
    events  = response.json()
    print(len(events))

    assert response.status_code == 200

    response = client.get("/events/dates/?planet_id=1")
    assert response.status_code == 200

    new_event = NewEvent(story= "test", event_date = "2021-07-30", planet_id=1, uuid=str(uuid.uuid4()) )
    response = client.post("/events/?planet_id=1", json=new_event.model_dump())
    assert response.status_code == 201

    response = client.get("/events/?planet_id=1")
    events = response.json()
    print(len(events))