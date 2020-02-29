from pprint import pprint


def toggle_tracks(spotify_client, desired_explicit_state):
    tracks = spotify_client.get_all_user_tracks()

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

    pprint(track_to_desired_track_map)
