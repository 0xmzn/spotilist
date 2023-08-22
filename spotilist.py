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

def write_tracks_to_files(dictionary, filename):
    with open(filename, 'w') as file:
        for key in dictionary.keys():
            file.write(key + '\n')

    file.close()    
    shutil.copy(filename, f"{filename}.bak")

filename="songs.txt"
write_tracks_to_files(tracks, filename)

def find_unique_lines(filename):
    file1 = filename
    file2 = f"{filename}.bak"
    with open(file1, 'r') as file1, open(file2, 'r') as file2:
        lines1 = set(line.strip() for line in file1)
        lines2 = set(line.strip() for line in file2)

    unique_lines = list(lines2 - lines1)

    return unique_lines


write_tracks_to_files(tracks, filename)
print(f"Please update {filename} and press enter")
input()
diff = find_unique_lines(filename)

def get_tracks_ids(diff, tracks):
    diff_id = []
    for i in diff:
        diff_id.append(tracks[i])
    return diff_id

diff_ids = get_tracks_ids(diff, tracks)
sp.playlist_remove_all_occurrences_of_items(chosen_playlist_id, diff_ids)