import asyncio
import json
import os
import uuid

from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from helper import get_utc_day
import db
from imageGenerator import *


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


@app.get("/events/")
def get_events(date : str | None = ""):
    return db.get_events(date)


@app.get("/events/dates")
def get_dates():
    return db.get_dates()

#should be call at the end of every day
#@app.put("/events/")
#def define_winner(date):
#    db_define_winner(date)
 #   resp = success=True
 #   return resp


class Event(BaseModel):
    event_id: str

@app.put("/events/")
def increase_vote(event: Event):
    db.increase_vote(event.event_id)
    resp = success=True
    return resp

@app.post("/events/")
def news(story : str):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Imagine a newspaper's  one sentence article based on this event: \"{story}\"."
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


    full_json = json.dumps(json_result)

    asyncio.run(db.add_event_to_world(json_result))

    return full_json


