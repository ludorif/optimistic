#  Copyright (c) 2025 Ludovic Riffiod
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, UTC

from backend import db
from backend import model
from backend import open_ai_manager
from fastapi import FastAPI, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.cron import CronTrigger

def define_winner():
    today = datetime.now(UTC)
    print("define_winner")
    db.define_winner(today.strftime("%Y-%m-%d"))

# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=23, minute=59)  # midnight every day
scheduler.add_job(define_winner, trigger)
scheduler.start()



app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        response_dict = open_ai_manager.generate_new_event(new_event.story)
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
