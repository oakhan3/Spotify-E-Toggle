import functools
import logging
from dataclasses import dataclass
from typing import List, Optional

import spotipy

from spotify_e_toggle.types import Playlist, Track

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
    ]

    def authenticate(self):
        token = spotipy.util.prompt_for_user_token(self.username, ",".join(self.scopes))
        self.client = spotipy.Spotify(auth=token)

    def search_tracks(self, query, limit=10):
        logger.info("Querying for %s, with limit %s", query, limit)
        response = self.client.search(q=query, type="track", limit=limit)
        return (Track.from_response(track) for track in response["tracks"]["items"])

    # NOTE: These methods could be abstracted out to a "user resource manager" classes
    def get_all_user_playlists(self):
        items = self._exhaust_pagination(self.client.current_user_playlists)
        return (Playlist.from_response(item) for item in items)

    def get_playlist_tracks(self, playlist_id):
        fn = functools.partial(self.client.playlist_tracks, playlist_id=playlist_id)
        items = self._exhaust_pagination(fn)

        return (Track.from_response(item["track"]) for item in items)

    def save_playlist_tracks(self, user_id, playlist_id, tracks: List[Track]):
        track_ids = [track.id for track in tracks]
        self.client.user_playlist_add_tracks(user_id, playlist_id, track_ids, position=0)

    def delete_playlist_tracks(self, user_id, playlist_id, tracks: List[Track]):
        track_ids = [track.id for track in tracks]
        self.client.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, track_ids)

    def get_all_user_tracks(self):
        items = self._exhaust_pagination(self.client.current_user_saved_tracks)
        return (Track.from_response(item["track"]) for item in items)

    def save_user_tracks(self, tracks: List[Track]):
        track_ids = [track.id for track in tracks]
        self.client.current_user_saved_tracks_add(track_ids)

    def delete_user_tracks(self, tracks: List[Track]):
        track_ids = [track.id for track in tracks]
        self.client.current_user_saved_tracks_delete(track_ids)

    def _exhaust_pagination(self, fn, limit=50, offset=0):
        next_ = ""
        items = []
        while next_ is not None:
            response = fn(limit=limit, offset=offset)
            next_ = response["next"]
            items += response["items"]
            logger.info(
                "Successfully retrieved items at offset %s, with limit %s", limit, offset,
            )
            offset += limit

        return items
