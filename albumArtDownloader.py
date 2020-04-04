

import keyring
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#establish api token credentials
clientID = "296f3ecbec394f5caab0198f4684ed95"
secret = keyring.get_password("spotify","296f3ecbec394f5caab0198f4684ed95")
#create credentials object
creds = SpotifyClientCredentials(client_id=clientID, client_secret=secret)

#create spotify object
spotify = spotipy.Spotify(client_credentials_manager=creds)

#define what you're searching for
kickass_metal_playlist_uri = "spotify:playlist:37i9dQZF1DWTcqUzwhNmKv"
result = spotify.playlist_cover_image("spotify:playlist:37i9dQZF1DWTcqUzwhNmKv")
print(result)

query = spotify.search('q=genre:metal', offset=0, type="album", market='US')
print(query)
query2=(query['albums']['items'])
#result2 = spotify.albums(query2)
print(query2)


#get the image link from the search results


f = open('albumartimages/test.jpg','wb')
f.write(requests.get('https://i.scdn.co/image/ab67706f00000002fadcea36eef98ee8761b8b39').content)
f.close()


#download and save image to albumart folder