import spotipy
import pandas as pd

from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

df = pd.read_csv("C:\\Users\\Christopher\\Documents\\UVM\\Junior Spring\\SE\\warmup\\data\\top50.csv",encoding='latin-1')

artist_names = set(df["Artist.Name"])

client_id = "bbc6324fcc26498ea4e5041cb9c2a18a"
client_secret = "0f5d2ea2192142e4855a7464fc79dc8c"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

valence = []
dance = []

for name in artist_names:

    ## Talking to spotify getting data we need
    result = sp.search(name) #search query
    artist_id = result['tracks']['items'][0]['artists'][0]['id']
    top_10 = sp.artist_top_tracks(artist_id, country='US')

    valence_total= 0
    dance_total = 0

    for track_num in range(0,10):
        song_id = top_10['tracks'][0]['id']
        features = sp.audio_features(song_id)
        valence_total += float(features[0]['valence'])
        dance_total += float(features[0]['danceability'])

    ## Getting avg for artist (formating stuff too)
    valence_avg = int((valence_total/10)*100)
    dance_avg = int((dance_total/10)*100)

    ## adding avg to parallel lists (formating stuff too)
    valence.append(valence_avg/100)
    dance.append(dance_avg/100)

final_dict = {"Artist":list(artist_names), "valence":valence, "dance": dance}
final_df = pd.DataFrame(final_dict)
final_df.to_csv("features.csv")
