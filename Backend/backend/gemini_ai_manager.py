#  Copyright (c) 2025 Ludovic Riffiod

import uuid
import json

from google import genai

from . import helper
from . import pexels_manager


def generate_new_event(story : str | None = ""):
    client = genai.Client()

    request = "Imagine a newspaper's one sentence article based on"
    if story == "":
        request += " a one sentence story (human like) you will generate."
    else:
        request += f" this event: \"{story}\"."

    request += """It should be overly optimistic and always climate positive."
    Propose only 1 choice. 
    Return a valid json with the title and the content.
    Do not return the story."""


    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=request
    )

    #clean response
    response_formatted =  response.text.replace("```json", "")
    response_formatted = response_formatted.replace("```", "")

    #print(response_formatted)

    response_dict = json.loads(response_formatted)
    response_dict["photoId"] = pexels_manager.get_photo_id(response_dict["title"])
    response_dict["date"] =  helper.get_utc_day()
    response_dict["votes"] = []

    return  response_dict

def generate_summary(all_events):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"Make a one or two sentences summary of this planet story based on all those events: \"{all_events}\"."
                 f"It should be overly optimistic and always climate positive."
    )

    response_formatted = response.text.replace("```json", "")
    response_formatted = response_formatted.replace("```", "")

    return response_formatted