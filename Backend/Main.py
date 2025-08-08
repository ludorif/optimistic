import asyncio
import json
import os
import uuid

from google import genai
from flask_cors import CORS
from flask import Flask, jsonify

from db import add_event_to_world, get_all_events
from imageGenerator import get_photo_id

os.environ["GEMINI_API_KEY"] = "AIzaSyDCmmQEnq-A1RdP-Nx4BqyCmKgl87_KHXI"


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

all_events = get_all_events()
print(all_events)

@app.route("/history")
def history():
    all_events = get_all_events()
    return jsonify(json.dumps(all_events))

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



    full_json = json.dumps(json_result)

    asyncio.run(add_event_to_world(json_result))

    return jsonify(full_json)