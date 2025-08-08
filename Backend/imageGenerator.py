# Import API class from pexels_api package
from pexels_api import API
# Type your Pexels API
PEXELS_API_KEY = 'L4qByXmvz7OO8u7oJtmWLioLd2KQm7VwVEkV0SAsOSaRySVHU5Tm4FtA'
# Create API object
api = API(PEXELS_API_KEY)
# Search five 'kitten' photos
api.search('kitten', page=1, results_per_page=1)
# Get photo entries
photos = api.get_entries()
# Loop the five photos
for photo in photos:
  # Print photographer
  print('Photographer: ', photo.photographer)
  # Print url
  print('Photo url: ', photo.url)
  # Print original size url
  print('Photo original size: ', photo.original)