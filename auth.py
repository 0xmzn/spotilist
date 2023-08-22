from dotenv import load_dotenv
import os
from spotipy import util

username = os.getenv("USERNAME")

def get_spotify_token(scope: str):
    """
    Retrieves a Spotify access token for the specified scope.
    """
    load_dotenv()
    
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    
    user_token = util.prompt_for_user_token(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        username=username,
        scope=scope
    )

    return user_token