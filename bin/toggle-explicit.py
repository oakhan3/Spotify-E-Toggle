#!/usr/bin/env python3
import argparse
import logging
import os

from spotify_e_toggle.spotify_client import SpotifyClient
from spotify_e_toggle.actions import (
    choose_playlist_id,
    toggle_user_saved_tracks,
    toggle_playlist_tracks,
    SAVED_TRACKS_ID,
)

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(
    description="Toggle user's saved tracks to be explicit or censored."
)
parser.add_argument("toggle", choices=["explicit", "censored"])


if __name__ == "__main__":
    args = parser.parse_args()
    desired_explicit_state = "explicit" == args.toggle

    username = os.environ["SPOTIFY_USERNAME"]

    spotify_client = SpotifyClient(username)
    spotify_client.authenticate()

    playlist_user_id, playlist_id = choose_playlist_id(spotify_client, username)

    if SAVED_TRACKS_ID == playlist_id:
        toggle_user_saved_tracks(spotify_client, desired_explicit_state)
    else:
        toggle_playlist_tracks(
            spotify_client, desired_explicit_state, playlist_user_id, playlist_id,
        )
