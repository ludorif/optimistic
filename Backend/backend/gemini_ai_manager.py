#  Copyright (c) 2025 Ludovic Riffiod

import uuid
import json

from google import genai

from backend import helper
from backend import pexels_manager






def generate_new_event(story : str):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"Imagine a newspaper's  one sentence article based on this event: \"{story}\"."
                 f"It should be overly optimistic and always climate positive."
                 f"Propose only 1 choice. "
                 f"Return a valid json with the title and the content."
    )

    #clean response
    response_formatted =  response.text.replace("```json", "")
    response_formatted = response_formatted.replace("```", "")

    response_dict = json.loads(response_formatted)
    response_dict["_id"] = str(uuid.uuid4())
    response_dict["photoId"] = pexels_manager.get_photo_id(response_dict["title"])
    response_dict["date"] =  helper.get_utc_day()
    response_dict["votes"] = []

    return  response_dict


