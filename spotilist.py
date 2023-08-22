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