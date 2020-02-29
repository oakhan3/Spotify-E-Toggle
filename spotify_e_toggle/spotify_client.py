import logging
from dataclasses import dataclass
from typing import Optional

import spotipy

from spotify_e_toggle.types import Track

logger = logging.getLogger(__name__)


@dataclass
class SpotifyClient:
    username: str
    client: Optional[spotipy.client.Spotify] = None

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
            logger.info(
                "Successfully retrieved user's saved tracks at offset %s, with limit %s",
                limit,
                offset,
            )
            offset += limit

        return (Track.from_response(track["track"]) for track in tracks)

    def search_tracks(self, query, limit=10):
        logger.info("Querying for %s, with limit %s", query, limit)
        response = self.client.search(q=query, type="track", limit=limit)
        return (Track.from_response(track) for track in response["tracks"]["items"])
