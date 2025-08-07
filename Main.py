import os
from google import genai

os.environ["GEMINI_API_KEY"] = "AIzaSyDCmmQEnq-A1RdP-Nx4BqyCmKgl87_KHXI"



from flask import Flask

app = Flask(__name__)

@app.route("/news/<input>")
def news(input):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Imagine a newspaper's overly optimistic short article based on this event: \"{input}\".Propose only 1 choice"
    )
    return f"<p>{response.text}</p>"