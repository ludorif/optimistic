import asyncio
import json
import os
import uuid

from google import genai
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request

from db import add_event_to_world, get_all_events, get_events_to_vote, increase_vote_db
from imageGenerator import get_photo_id

os.environ["GEMINI_API_KEY"] = "AIzaSyDCmmQEnq-A1RdP-Nx4BqyCmKgl87_KHXI"


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}}, methods=["GET", "POST"])

all_events = get_all_events()
print(all_events)

@app.route("/history")
def history():
    all_events = get_all_events()
    return jsonify(json.dumps(all_events))

@app.route("/to_vote")
def to_vote():
    events_to_vote = get_events_to_vote()
    return jsonify(json.dumps(events_to_vote))


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
        contents=f"Imagine a newspaper's overly optimistic one sentence article based on this event: \"{request_text}\"."
                 f"Propose only 1 choice. "
                 f"Return a valid json with the title and the content."
    )

    #clean response
    response_formatted =  response.text.replace("```json", "")
    response_formatted = response_formatted.replace("```", "")

    json_result = json.loads(response_formatted)
    json_result["_id"] = str(uuid.uuid4())
    json_result["photoId"] = get_photo_id(json_result["title"])
    json_result["state"] = "to_vote"
    json_result["votes"] = 0

    full_json = json.dumps(json_result)

    asyncio.run(add_event_to_world(json_result))

    return jsonify(full_json)