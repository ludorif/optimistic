#  Copyright (c) 2025 Ludovic Riffiod
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, UTC, timedelta

from sqlalchemy.orm.session import Session

#from . import mongo_db
from . import model
from . import gemini_ai_manager
from . import voice_over_manager
from fastapi import FastAPI, Response, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.triggers.cron import CronTrigger
from . import comic_ai_manager
from . import sqlite_db_manager
from .sqlite_db_manager import get_db


app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://optimistic-1.onrender.com",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
TIMEZONE = ZoneInfo("UTC")
scheduler = AsyncIOScheduler(timezone=TIMEZONE)

def get_summary():
    all_events = sqlite_db_manager.get_all_events_story(1)
    all_events_str = ""
    for event in all_events:
        all_events_str = all_events_str + "\""+ event['content'] + "\","
    return gemini_ai_manager.generate_summary(all_events_str)

#@app.get("/define_winner/")
async def define_winner():
    today = datetime.now(UTC)
    print("define_winner")
    success = sqlite_db_manager.define_all_winners()
    #if success ==  True:
    #    await generate_summary_and_comic()


def main():
    print("starting")

    for hour_int in range(8, 14, 2):
        trigger = CronTrigger(hour=hour_int, minute=0, timezone=TIMEZONE)
        scheduler.add_job(create_fake_event, trigger)

    for hour_int in range(14, 22, 2):
        trigger = CronTrigger(hour=hour_int, minute=0, timezone=TIMEZONE)
        scheduler.add_job(fake_vote, trigger)


    trigger = CronTrigger(hour=23, minute=59)
    scheduler.add_job(define_winner, trigger, timezone=TIMEZONE)

    #to test
    #scheduler.add_job(define_winner, 'date', run_date=datetime.now() + timedelta(seconds=1))


    scheduler.start()
    print("started")



@app.get("/summary/")
def get_summary():
    return mongo_db.get_summary(1)

async def generate_summary_and_comic():
    summary_content = get_summary()
    mongo_db.update_summary(1, summary_content)
    await comic_ai_manager.generate(summary_content)

# Ensure the scheduler shuts down properly on application exit.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()


@app.get("/events/")
def get_events(planet_id : int, date : str | None = "", session: Session = Depends(get_db)):
    return sqlite_db_manager.get_events(planet_id, date, session)

@app.get("/events/dates/")
def get_dates(planet_id : int, session: Session = Depends(get_db)):
    return sqlite_db_manager.get_dates(planet_id, session)

@app.post("/events/")
async def add_new_event(new_event: model.NewEvent, response: Response, session: Session = Depends(get_db)):
    return await sqlite_db_manager.add_new_event(new_event, response, session)

@app.put("/events/")
def increase_vote(event: model.ExistingEvent, request: Request,  response: Response, session: Session = Depends(get_db)):
    status_code, message = sqlite_db_manager.increase_vote(event, session)
    response.status_code = status_code
    return {"message": message}


@app.get("/winners/")
def get_winners(session: Session = Depends(get_db)):
    return sqlite_db_manager.get_winners(session)

@app.get("/voiceOver/")
def get_voice_over(content : str, session: Session = Depends(get_db)):
    return voice_over_manager.generate_text(content)

@app.get("/planets/")
def get_planets(session: Session = Depends(get_db)):
    return sqlite_db_manager.get_planets(session)

@app.post("/planets/")
def post_planets(new_planet: model.Planet, session: Session = Depends(get_db)):
    planet_id = sqlite_db_manager.post_planet(new_planet, session)
    return {"planet_id": planet_id}


async def create_fake_event():
    session: Session = get_db()
    await sqlite_db_manager.create_fake_event(session)

def fake_vote():
    session: Session = get_db()
    sqlite_db_manager.fake_vote(session)


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

main()
