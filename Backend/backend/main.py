import asyncio
import json

import db
import model
import open_ai_manager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(redirect_slashes=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/winners/")
def get_winners():
    return db.get_winners()

@app.get("/events/")
def get_events(date : str | None = ""):
    return db.get_events(date)

@app.get("/events/dates")
def get_dates():
    return db.get_dates()

@app.post("/events/")
def news(story : str):
    response_dict = open_ai_manager.generate_new_event(story)
    asyncio.run(db.add_event_to_world(response_dict))
    return json.dumps(response_dict)

@app.put("/events/")
def increase_vote(event: model.Event):
    db.increase_vote(event.event_id)
    resp = success=True
    return resp


#should be call at the end of every day
#@app.put("/events/")
#def define_winner(date):
#    db_define_winner(date)
 #   resp = success=True
 #   return resp
