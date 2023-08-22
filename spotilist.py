from auth import *
import spotipy


user_token = get_spotify_token("playlist-modify-private")
sp = spotipy.Spotify(auth=user_token)


def get_playlists(username):
    playlists = sp.user_playlists(username)
    playlist_dict = {}
    for playlist in playlists['items']:
        playlist_dict[playlist['name']] = playlist['id']
    
    return playlist_dict