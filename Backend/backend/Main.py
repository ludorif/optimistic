import asyncio
import json
import os
import uuid

from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel



from helper import get_utc_day
from db import add_event_to_world, get_all_events, get_events_to_vote, increase_vote_db, db_get_dates, db_define_winner
from imageGenerator import get_photo_id

os.environ["GEMINI_API_KEY"] = "AIzaSyDCmmQEnq-A1RdP-Nx4BqyCmKgl87_KHXI"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Date(BaseModel):
    event_id: str


@app.get("/history/")
def history(date : str | None = ""):
    all_events = get_all_events(date)
    return json.dumps(all_events)

@app.get("/to_vote")
def to_vote():
    events_to_vote = get_events_to_vote()
    return json.dumps(events_to_vote)

@app.get("/get_dates")
def get_dates():
    dates = db_get_dates()
    return json.dumps(dates)

#should be call at the end of every day
@app.get("/define_winner/<date>")
def define_winner(date):
    db_define_winner(date)
    resp = success=True
    return resp


class Event(BaseModel):
    event_id: str

@app.post("/increase_vote")
def increase_vote(event: Event):
    increase_vote_db(event.event_id)
    resp = success=True
    return resp

@app.get("/news/<request_text>")
def news(request_text):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Imagine a newspaper's  one sentence article based on this event: \"{request_text}\"."
                 f"It should be overly optimistic and always climate positive."
                 f"Propose only 1 choice. "
                 f"Return a valid json with the title and the content."
    )

    #clean response
    response_formatted =  response.text.replace("```json", "")
    response_formatted = response_formatted.replace("```", "")

    json_result = json.loads(response_formatted)
    json_result["_id"] = str(uuid.uuid4())
    json_result["photoId"] = get_photo_id(json_result["title"])
    json_result["date"] =  get_utc_day()
    json_result["votes"] = 0

    print(get_utc_day())

    full_json = json.dumps(json_result)

    asyncio.run(add_event_to_world(json_result))

    return full_json


