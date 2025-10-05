#  Copyright (c) 2025 Ludovic Riffiod
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, UTC

from . import db
from . import model
from . import gemini_ai_manager
from . import voice_over_manager
from fastapi import FastAPI, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.cron import CronTrigger
from . import comic_ai_manager

app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_summary():
    all_events = db.get_all_events_story()
    all_events_str = ""
    for event in all_events:
        all_events_str = all_events_str + "\""+ event['content'] + "\","
    return gemini_ai_manager.generate_summary(all_events_str)

def define_winner():
    today = datetime.now(UTC)
    print("define_winner")
    db.define_winner(today.strftime("%Y-%m-%d"))


def main():
    # Set up the scheduler
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=23, minute=59)  # midnight every day
    scheduler.add_job(define_winner, trigger)
    scheduler.start()




@app.get("/summary/")
async def generate_summary():
    return db.get_summary(1)

@app.post("/summary/")
async def generate_summary():
    summary_content = get_summary()
    db.update_summary(1, summary_content)
    #await comic_ai_manager.generate(summary_content)

# Ensure the scheduler shuts down properly on application exit.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()


@app.get("/events/")
def get_events(date : str | None = ""):
    return db.get_events(date)

@app.get("/events/dates")
def get_dates():
    return db.get_dates()

@app.post("/events/")
def add_new_event(new_event: model.NewEvent, request: Request, response: Response):
    number_of_events, user_already_participated = db.check_current_events(new_event.event_date, new_event.uuid)

    if user_already_participated:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message":"Already participated"}
    elif number_of_events >= 3:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Enough events for today"}
    else:
        response_dict = gemini_ai_manager.generate_new_event(new_event.story)
        response_dict["client_uuid"]= new_event.uuid
        asyncio.run(db.add_event_to_world(response_dict))
        response.status_code = status.HTTP_201_CREATED
        return {"message": "New event added"}

@app.put("/events/")
def increase_vote(event: model.ExistingEvent, request: Request,  response: Response):
    status_code, message = db.increase_vote(event.event_id, event.uuid)
    response.status_code = status_code
    return {"message": message}


@app.get("/winners/")
def get_winners():
    return db.get_winners()

@app.get("/voiceOver/")
def get_voice_over(content : str):
    return voice_over_manager.generate_text(content)



@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=model.HealthCheck,
)
def get_health() -> model.HealthCheck:
    db.get_health()
    return model.HealthCheck(status="OK")

main()
