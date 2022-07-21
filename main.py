from bs4 import BeautifulSoup
import requests
import datetime

while True:
    date_input = input("What date would you like to go back to? (YYYY-MM-DD)")
    # date_input = "1997-05-26"
    URL = f"https://www.billboard.com/charts/hot-100/{date_input}/"
    response = requests.get(URL)
    if response.status_code != 404:
        break
    else:
        print("please try again and follow the YYYY-MM-DD format, include dashes")

website = response.text
soup = BeautifulSoup(website, "html.parser")
# print(soup.prettify())

song_titles = soup.select(selector="li #title-of-a-story")
# song_titles = soup.findAll(name="li", id="title-of-a-story")
# print(song_titles)
top_100_song = [song.get_text().strip() for song in song_titles]
print(top_100_song)

CLIENT_ID = "426e184b9c7744dca8145b759db4ceec"
CLIENT_SECRET = "38535f7ffd644994ad8f0412b8f2a156"

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date_input.split("-")[0]
for song in top_100_song:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)