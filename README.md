# Spotify E-Toggle

Toggle your Spotify saved tracks, or any of your playlists, to be explicit or censored!

## Instructions

1. Set the following environment variables:

    ```shell
    $ export SPOTIFY_USERNAME="<Your Spotify Username"

    # Generate by creating an app on the Spotify API Dashboard
    $ export SPOTIPY_CLIENT_ID=""
    $ export SPOTIPY_CLIENT_SECRET=""

    # Configure to a valid URL in your apps configuration on the Spotify API Dashboard
    # The actual url does not have to be working
    # Example URL: http://localhost:8000/
    $ export SPOTIPY_REDIRECT_URI=""
    ```

1. Clone/download this repo.

1. pip install this package in a Python 3.6.1+ env:

    ```
    $ pwd
    .../spotify-e-toggle

    $ pip install .
    ```

1. Run the script:

    ```shell
    $ ./bin/toggle-explicit.py <explicit|censored>

    DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.spotify.com:443
    DEBUG:urllib3.connectionpool:https://api.spotify.com:443 "GET /v1/me/playlists?limit=50&offset=0 HTTP/1.1" 200 None
    INFO:spotify_e_toggle.spotify_client:Successfully retrieved items at offset 50, with limit 0
    DEBUG:urllib3.connectionpool:https://api.spotify.com:443 "GET /v1/me/playlists?limit=50&offset=50 HTTP/1.1" 200 None
    INFO:spotify_e_toggle.spotify_client:Successfully retrieved items at offset 50, with limit 50

    +------------------------+----------------------------+------------+-----------------+----------+
    | ID                     | Name                       | Owner      | Collaborative   | Public   |
    |------------------------+----------------------------+------------+-----------------+----------|
    | your-saved-tracks      | Your Saved Tracks          | oakhan3    | False           | False    |
    | dfsjhsd_fake_dhfddjkjd | Soccer Fever               | 731fake233 | True            | False    |
    | 2sjdhkd_fake_ljsdhbdsk | STUMBLR                    | oakhan3    | False           | True     |
    | fdskjhd_fake_skghjfjkd | Life After – Ace Hood      | oakhan3    | False           | True     |
    | fdskjhf_fake_ksjdfskjd | DaBump                     | oakhan3    | False           | True     |
    | sdfjhjk_fake_shkjfdjsh | Discover Weekly Archive    | oakhan3    | False           | False    |
    | dfshjsf_fake_sfksdfhjj | Poor Kid Rich Soul         | oakhan3    | False           | True     |
    | dsfkjhs_fake_fjjdsjdfd | Summer 2015                | oakhan3    | False           | True     |
    | dsfhfsd_fake_fshjkdfsh | Liked from Radio           | oakhan3    | False           | False    |
    | dfsjhdf_fake_jkhjdshfh | My Shazam Tracks           | oakhan3    | False           | True     |
    | dsjfhfj_fake_sfhjfkdsj | Starred                    | oakhan3    | False           | False    |
    +------------------------+----------------------------+------------+-----------------+----------+

    What Playlist ID should be toggled: <Paste a Playlist ID here>
    ```
