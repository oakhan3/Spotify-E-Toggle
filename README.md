# Spotify E-Toggle

Automatically toggle your Spotify saved tracks/playlists between explicit and censored!

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
    ```
