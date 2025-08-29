#  Copyright (c) 2025 Ludovic Riffiod
import os

from pexels_api import API

def get_photo_id(title):
    pexels_api_key = uri = os.environ["pexels_api_key"]
    api = API(pexels_api_key)

    api.search(f'{title}', page=1, results_per_page=1)

    photos = api.get_entries()

    return photos[0].id