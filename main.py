import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import helper
import random

scope = ('playlist-modify-public', 'playlist-modify-private', 'playlist-read-private')
username = config.username

token = SpotifyOAuth(scope=scope, username=username)
sp = spotipy.Spotify(auth_manager=token)

# Create a playlist
playlist_name = input("Enter a name for your playlist: ")
playlist_description = "Created by MergePlaylists script and Spotify API"
sp.user_playlist_create(username, playlist_name, public=True, description=playlist_description)

# Get current user playlists
result=sp.current_user_playlists()
playlists = {}
for item in result['items']:
    description = item['description']
    if 'MergePlaylists' not in description:
        name = item['name']
        playlists[name] = item['id']

# Get playlist tracks
tracks = []
for playlist_name in playlists:
    playlist_tracks = helper.get_playlist_tracks(sp, username,playlists[playlist_name])
    for playlist_track in playlist_tracks:
        if 'spotify:local' not in playlist_track['track']['uri']:
            tracks.append(playlist_track['track']['uri'])
random.shuffle(tracks)

# # Add tracks to playlist
prePlaylist = sp.user_playlists(user=username)
playlist_id = prePlaylist['items'][0]['id']
while tracks:
    results = sp.user_playlist_add_tracks(username, playlist_id, tracks[:100], position=None)
    tracks = tracks[100:]

print("Done!")