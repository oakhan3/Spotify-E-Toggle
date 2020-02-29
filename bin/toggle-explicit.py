#!/usr/bin/env python3
import argparse
import os
from pprint import pprint

from spotify_e_toggle.spotify_client import SpotifyClient

parser = argparse.ArgumentParser(
    description="Toggle user's saved tracks to be explicit or censored songs."
)
parser.add_argument("toggle", choices=["explicit", "censored"])

if __name__ == "__main__":
    args = parser.parse_args()
    desired_explicit_state = "explicit" == args.toggle

    username = os.environ["SPOTIFY_USERNAME"]

    spotify_client = SpotifyClient(username)
    spotify_client.authenticate()

    tracks = spotify_client.get_all_user_tracks()

    bad_tracks = (track for track in tracks if track.explicit != desired_explicit_state)

    track_to_desired_track_map = {}
    for track in bad_tracks:
        alternative_tracks = spotify_client.search_tracks(query=track.search_query, limit=10)

        for alternative_track in alternative_tracks:
            if alternative_track.explicit == desired_explicit_state:
                track_to_desired_track_map[track] = alternative_track

    pprint(track_to_desired_track_map)
