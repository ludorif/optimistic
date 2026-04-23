#  Copyright (c) 2025 Ludovic Riffiod
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import Session

from . import model
from . import gemini_ai_manager
from . import voice_over_manager
from . import sqlite_db_manager
from .sqlite_db_manager import get_db
from .auth import create_session_token, get_current_uuid

logger = logging.getLogger(__name__)

_SCHEDULER_SECRET = os.environ.get("SCHEDULER_SECRET", "")


def _verify_scheduler(x_scheduler_secret: str = Header(...)):
    if not _SCHEDULER_SECRET or x_scheduler_secret != _SCHEDULER_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):
    logger.info("starting")
    yield
    logger.info("stopped")


app = FastAPI(redirect_slashes=False, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://optimistic-1.onrender.com",
        "https://optimistic-frontend-50282192891.europe-west1.run.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_summary(planet_id: int, session: Session):
    all_events = sqlite_db_manager.get_all_events_story(planet_id, session)
    all_events_str = ""
    for event in all_events:
        all_events_str = all_events_str + "\"" + event['content'] + "\","
    return gemini_ai_manager.generate_summary(all_events_str)


# --- Scheduler endpoints (called by Cloud Scheduler) ---

@app.post("/scheduler/fake-event/")
async def trigger_fake_event(session: Session = Depends(get_db), _=Depends(_verify_scheduler)):
    await sqlite_db_manager.create_fake_event(session)
    return {"message": "fake event created"}

@app.post("/scheduler/fake-vote/")
def trigger_fake_vote(session: Session = Depends(get_db), _=Depends(_verify_scheduler)):
    sqlite_db_manager.fake_vote(session)
    return {"message": "fake vote done"}

@app.post("/scheduler/define-winner/")
def trigger_define_winner(session: Session = Depends(get_db), _=Depends(_verify_scheduler)):
    logger.info("define_winner triggered")
    sqlite_db_manager.define_all_winners(session)
    return {"message": "winner defined"}

@app.post("/scheduler/generate-summary/")
async def trigger_generate_summary(session: Session = Depends(get_db), _=Depends(_verify_scheduler)):
    planets = sqlite_db_manager.get_planets(session)
    for planet in planets:
        planet_id = planet['id']
        summary_content = create_summary(planet_id, session)
        sqlite_db_manager.update_summary(planet_id, summary_content, session)
    return {"message": "summaries updated"}


# --- Public endpoints ---

@app.get("/session/")
def get_session():
    _, token = create_session_token()
    return {"token": token}

@app.get("/summary/")
def get_summary(planet_id: int, session: Session = Depends(get_db)):
    return sqlite_db_manager.get_summary(planet_id, session)

@app.get("/events/")
def get_events(planet_id: int, date: str | None = "", session: Session = Depends(get_db)):
    return sqlite_db_manager.get_events(planet_id, date, session)

@app.get("/events/dates/")
def get_dates(planet_id: int, session: Session = Depends(get_db)):
    return sqlite_db_manager.get_dates(planet_id, session)

@app.post("/events/")
async def add_new_event(new_event: model.NewEvent, response: Response, session: Session = Depends(get_db), uuid: str = Depends(get_current_uuid)):
    new_event.uuid = uuid
    return await sqlite_db_manager.add_new_event(new_event, response, session)

@app.put("/events/")
def increase_vote(event: model.ExistingEvent, response: Response, session: Session = Depends(get_db), uuid: str = Depends(get_current_uuid)):
    event.uuid = uuid
    status_code, message = sqlite_db_manager.increase_vote(event, session)
    response.status_code = status_code
    return {"message": message}

@app.get("/winners/")
def get_winners(session: Session = Depends(get_db)):
    return sqlite_db_manager.get_winners(session)

@app.get("/voiceOver/")
def get_voice_over(content: str, session: Session = Depends(get_db)):
    return voice_over_manager.generate_text(content)

@app.get("/planets/")
def get_planets(session: Session = Depends(get_db)):
    return sqlite_db_manager.get_planets(session)

@app.post("/planets/")
def post_planets(new_planet: model.Planet, session: Session = Depends(get_db)):
    planet_id = sqlite_db_manager.post_planet(new_planet, session)
    return {"planet_id": planet_id}

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=model.HealthCheck,
)
def get_health(session: Session = Depends(get_db)) -> model.HealthCheck:
    sqlite_db_manager.get_health(session)
    return model.HealthCheck(status="OK")
