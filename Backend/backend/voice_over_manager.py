#  Copyright (c) 2025 Ludovic Riffiod
#
import json
import os
import random
import requests

def generate_text(content):
    headers = {
        'Authorization': f'Bearer {os.environ["VOICE_MAKER_API_KEY"]}',
        'Content-Type': 'application/json',
    }

    voice_id = 'proplus-Lucy' if random.random() >= 0.5  else "proplus-RyanCooper"

    json_data = {
        'Engine': 'neural',
        'VoiceId': voice_id,
        'LanguageCode': 'en-GB',
        'Text': content,
        'OutputFormat': 'mp3',
        'SampleRate': '48000',
        'Effect': 'default',
        'MasterVolume': '0',
        'MasterSpeed': '0',
        'MasterPitch': '0',
    }

    response = requests.post('https://developer.voicemaker.in/voice/api', headers=headers, json=json_data)
    return json.dumps(response.json())