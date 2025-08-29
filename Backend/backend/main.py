#  Copyright (c) 2025 Ludovic Riffiod
import asyncio

from backend import db
from backend import model
from backend import open_ai_manager
from fastapi import FastAPI, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/events/")
def get_events(date : str | None = ""):
    return db.get_events(date)

@app.get("/events/dates")
def get_dates():
    return db.get_dates()

@app.post("/events/")
def add_new_event(new_event: model.NewEvent, request: Request, response: Response):
    client_ip = request.client.host
    number_of_events, user_already_participated = db.check_current_events(new_event.event_date, client_ip)

    if user_already_participated:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message":"Already participated"}
    elif number_of_events >= 3:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Enough events for today"}
    else:
        response_dict = open_ai_manager.generate_new_event(new_event.story)
        response_dict["client_ip"]=client_ip
        asyncio.run(db.add_event_to_world(response_dict))
        response.status_code = status.HTTP_201_CREATED
        return {"message": "New event added"}

@app.put("/events/")
def increase_vote(event: model.ExistingEvent, request: Request,  response: Response):
    client_ip = request.client.host
    success = db.increase_vote(event.event_id, client_ip)
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "Vote added"}
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Already participated"}


@app.get("/winners/")
def get_winners():
    return db.get_winners()

#should be call at the end of every day
@app.put("/winners/")
def define_winner(date : model.Date, response: Response):
    db.define_winner(date.selectedDate)
    response.status_code = status.HTTP_200_OK

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
