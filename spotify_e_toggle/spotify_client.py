from dataclasses import dataclass
from types import Optional

import spotipy


@dataclass
class SpotifyClient:
    username = str
    client = Optional[spotipy.client.Spotify] = None

    scopes = [
        "user-top-read",
        "user-read-recently-played",
        "user-library-modify",
        "user-library-read",
        "playlist-read-private",
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-collaborative",
        "user-read-private",
        "user-read-email",
    ]

    def authenticate(self):
        token = spotipy.util.prompt_for_user_token(self.username, ",".join(self.scopes))
        self.client = spotipy.Spotify(auth=token)

    def get_all_user_tracks(self, limit=50, offset=0):
        next_ = ""
        tracks = []
        while next_ is not None:
            response = self.client.current_user_saved_tracks(limit=limit, offset=offset)

            next_ = response["next"]
            tracks += response["items"]
            offset += limit

        return tracks
