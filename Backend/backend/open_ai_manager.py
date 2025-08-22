import uuid
import json
import os
from google import genai
from backend import helper
from backend import pexels_manager

os.environ["GEMINI_API_KEY"] = "AIzaSyDCmmQEnq-A1RdP-Nx4BqyCmKgl87_KHXI"

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
    response_dict["photoId"] = get_photo_id(response_dict["title"])
    response_dict["date"] =  herlper.get_utc_day()
    response_dict["votes"] = 0

    return  response_dict


