import logging
from pprint import pformat

from tabulate import tabulate

logger = logging.getLogger(__name__)

SAVED_TRACKS_ID = "your-saved-tracks"


def choose_playlist_id(spotify_client, username):
    playlists = spotify_client.get_all_user_playlists()

    playlist_id_user_id_map = {SAVED_TRACKS_ID: username}
    rows = [[SAVED_TRACKS_ID, "Your Saved Tracks", username, "False", "False"]]

    for playlist in playlists:
        if playlist.collaborative or playlist.owner_id == username:
            rows.append(
                [
                    playlist.id,
                    playlist.name,
                    playlist.owner_id,
                    str(playlist.collaborative),
                    str(playlist.public),
                ]
            )
            playlist_id_user_id_map[playlist.id] = playlist.owner_id

    print(
        tabulate(rows, headers=["ID", "Name", "Owner", "Collaborative", "Public"], tablefmt="psql")
    )

    chosen_playlist_id = input("\nWhat Playlist ID should be toggled: ")
    if chosen_playlist_id not in playlist_id_user_id_map:
        raise ValueError("Invalid Playlist ID")

    return playlist_id_user_id_map[chosen_playlist_id], chosen_playlist_id


def toggle_user_saved_tracks(spotify_client, desired_explicit_state):
    tracks = spotify_client.get_all_user_tracks()

    desired_tracks, undesired_tracks = _generate_track_to_desired_track_map(
        spotify_client, tracks, desired_explicit_state
    )

    spotify_client.save_user_tracks(desired_tracks)
    spotify_client.delete_user_tracks(undesired_tracks)


def toggle_playlist_tracks(spotify_client, desired_explicit_state, playlist_user_id, playlist_id):
    tracks = spotify_client.get_playlist_tracks(playlist_id)

    desired_tracks, undesired_tracks = _generate_track_to_desired_track_map(
        spotify_client, tracks, desired_explicit_state
    )

    spotify_client.save_playlist_tracks(playlist_user_id, playlist_id, desired_tracks)
    spotify_client.delete_playlist_tracks(playlist_user_id, playlist_id, undesired_tracks)


def _generate_track_to_desired_track_map(spotify_client, tracks, desired_explicit_state):
    bad_tracks = (track for track in tracks if track.explicit != desired_explicit_state)

    track_to_desired_track_map = {}
    for track in bad_tracks:
        alternative_tracks = spotify_client.search_tracks(query=track.search_query, limit=10)

        for alternative_track in alternative_tracks:
            if (
                alternative_track.explicit == desired_explicit_state
                and alternative_track.is_appropriate_variant_of(track)
            ):
                track_to_desired_track_map[track] = alternative_track
                break

    logger.info(
        "Mapping from current tracks to desired tracks:\n%s",
        pformat(track_to_desired_track_map, indent=4),
    )

    desired_tracks = track_to_desired_track_map.values()
    undesired_tracks = track_to_desired_track_map.keys()

    return desired_tracks, undesired_tracks
