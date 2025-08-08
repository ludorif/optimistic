import json
import os
from google import genai
from flask_cors import CORS
from flask import Flask, jsonify
# Import API class from pexels_api package
from pexels_api import API
# Type your Pexels API
PEXELS_API_KEY = 'L4qByXmvz7OO8u7oJtmWLioLd2KQm7VwVEkV0SAsOSaRySVHU5Tm4FtA'
api = API(PEXELS_API_KEY)


os.environ["GEMINI_API_KEY"] = "AIzaSyDCmmQEnq-A1RdP-Nx4BqyCmKgl87_KHXI"


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/news/<input>")
def news(input):
    client = genai.Client()


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Imagine a newspaper's overly optimistic one sentence article based on this event: \"{input}\"."
                 f"Propose only 1 choice. "
                 f"Return a valid json with the title and the content."
    )


    response_formatted =  response.text.replace("```json", "")
    response_formatted = response_formatted.replace("```", "")

    jsonResult = json.loads(response_formatted)

    api.search(f'{jsonResult["title"]}', page=1, results_per_page=1)


    photos = api.get_entries()

    idJson = {"photoId": photos[0].id}
    jsonResult.update(idJson)

    return jsonify(json.dumps(jsonResult))