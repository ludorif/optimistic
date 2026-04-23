#  Copyright (c) 2025 Ludovic Riffiod
import os

from pexels_api import API

def get_photo_id(title) -> int | None:
    pexels_api_key = os.environ["PEXELS_API_KEY"]
    api = API(pexels_api_key)

    api.search(f'{title}', page=1, results_per_page=1)

    photos = api.get_entries()

    if len(photos) == 0:
        return None

    return photos[0].id