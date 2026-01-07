#  Copyright (c) 2025 Ludovic Riffiod
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, UTC, timedelta

#from . import mongo_db
from . import model
from . import gemini_ai_manager
from . import voice_over_manager
from fastapi import FastAPI, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.triggers.cron import CronTrigger
from . import comic_ai_manager
from . import sqlite_db_manager
from .model import NewEvent
import asyncio


app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
scheduler = AsyncIOScheduler()

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
    success = sqlite_db_manager.define_winner(today.strftime("%Y-%m-%d"))
    if success ==  True:
        await generate_summary_and_comic()



def main():
    print("starting")

    trigger = CronTrigger(hour=23, minute=59)  # midnight every day
    scheduler.add_job(define_winner, trigger)
    sqlite_db_manager.create_all_tables()
    print("started")
    scheduler.add_job(create_fake_event, 'date', run_date=datetime.now() + timedelta(seconds=1))
    scheduler.start()

async def create_fake_event():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    fake_new_event: model.NewEvent = NewEvent(story="test", event_date=today.strftime("%Y-%m-%d %H:%M:%S.%f"), uuid = str(uuid.uuid4()), planet_id = 1)
    response : Response = Response()
    await add_new_event(fake_new_event, response)
    print(response.status_code)



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
def get_events(planet_id : int, date : str | None = ""):
    return sqlite_db_manager.get_events(planet_id, date)

@app.get("/events/dates")
def get_dates():
    return sqlite_db_manager.get_dates()

@app.post("/events/")
async def add_new_event(new_event: model.NewEvent, response: Response):
    number_of_events, user_already_participated = sqlite_db_manager.check_current_events(new_event.event_date, new_event.uuid)

    print("number_of_events ", number_of_events)

    if user_already_participated:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message":"Already participated"}
    elif number_of_events >= 3:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Enough events for today"}
    else:
        await add_new_event_internal(new_event)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "New event added"}

async def add_new_event_internal(new_event: model.NewEvent):
    response_dict = gemini_ai_manager.generate_new_event(new_event.story)
    await sqlite_db_manager.add_event_to_world(response_dict, new_event.uuid, new_event.planet_id)


@app.put("/events/")
def increase_vote(event: model.ExistingEvent, request: Request,  response: Response):
    print(event)
    status_code, message = sqlite_db_manager.increase_vote(event.event_id, event.uuid)
    response.status_code = status_code
    return {"message": message}


@app.get("/winners/")
def get_winners():
    return sqlite_db_manager.get_winners()

@app.get("/voiceOver/")
def get_voice_over(content : str):
    return voice_over_manager.generate_text(content)

@app.get("/planets/")
def get_planets():
    return sqlite_db_manager.get_planets()

@app.post("/planets/")
def post_planets(new_planet: model.Planet, response: Response):
    planet_id = sqlite_db_manager.post_planet(new_planet)
    return {"planet_id": planet_id}


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=model.HealthCheck,
)
def get_health() -> model.HealthCheck:
    sqlite_db_manager.get_health()
    return model.HealthCheck(status="OK")

main()
