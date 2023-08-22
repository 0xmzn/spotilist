from auth import *
import spotipy
import shutil


user_token = get_spotify_token("playlist-modify-private")
sp = spotipy.Spotify(auth=user_token)


def get_playlists(username):
    playlists = sp.user_playlists(username)
    playlist_dict = {}
    for playlist in playlists['items']:
        playlist_dict[playlist['name']] = playlist['id']
    
    return playlist_dict

user_playlists = get_playlists(username)

def get_chosen_playlist(dictionary):
    print("Available Playlists:")
    for i, key in enumerate(dictionary.keys(), start=1):
        print(f"{i}. {key}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to the chosen playlist: "))
            if 1 <= choice <= len(dictionary):
                selected_key = list(dictionary.keys())[choice - 1]
                return dictionary[selected_key]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def parse_tracks(tracks_dict: dict, tracks_object):
    for i in tracks_object['items']:
        tracks_dict[i['track']['name']] = i['track']['id']
    return tracks_dict

chosen_playlist_id = get_chosen_playlist(user_playlists)

tracks_object = sp.playlist_tracks(playlist_id=chosen_playlist_id)
tracks_number = tracks_object['total']
tracks = {}

tracks_pages = tracks_number // 100
for i in range(0, tracks_pages+1):
    new_tracks = sp.playlist_tracks(chosen_playlist_id, offset=(100 * i))
    parse_tracks(tracks, new_tracks)