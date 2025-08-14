import asyncio
import json
import os
import uuid

from google import genai
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request

from helper import get_utc_day
from db import add_event_to_world, get_all_events, get_events_to_vote, increase_vote_db, db_get_dates, db_define_winner
from imageGenerator import get_photo_id

os.environ["GEMINI_API_KEY"] = "AIzaSyDCmmQEnq-A1RdP-Nx4BqyCmKgl87_KHXI"


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}}, methods=["GET", "POST"])


@app.route("/history/<date>")
def history(date):
    all_events = get_all_events(date)
    return jsonify(json.dumps(all_events))

@app.route("/to_vote")
def to_vote():
    events_to_vote = get_events_to_vote()
    return jsonify(json.dumps(events_to_vote))

@app.route("/get_dates")
def get_dates():
    dates = db_get_dates()
    return jsonify(json.dumps(dates))

#should be call at the end of every day
@app.route("/define_winner/<date>")
def define_winner(date):
    db_define_winner(date)
    resp = jsonify(success=True)
    return resp


@app.route("/increase_vote", methods=["POST"])
def increase_vote():
    increase_vote_db(request.json['event_id'])
    resp = jsonify(success=True)
    return resp

@app.route("/news/<request_text>")
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

    return jsonify(full_json)


