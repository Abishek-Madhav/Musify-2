import requests

# Define the URL and headers
url = 'https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud'
headers = {
    'x-rapidapi-host': 'spotify-scraper.p.rapidapi.com',
    'x-rapidapi-key': '057f69f4a6mshc4b580a0702816bp1895a1jsnc76ab04306a0'
}

# Define the query parameters
params = {
    'track': 'Photograph Ed Sheeran',
    'quality': 'sq'
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    print(data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
