from pexels_api import API

def get_photo_id(title):
    pexels_api_key = 'L4qByXmvz7OO8u7oJtmWLioLd2KQm7VwVEkV0SAsOSaRySVHU5Tm4FtA'
    api = API(pexels_api_key)

    api.search(f'{title}', page=1, results_per_page=1)

    photos = api.get_entries()

    return photos[0].id