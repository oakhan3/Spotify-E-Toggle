from dataclasses import dataclass
from typing import List


@dataclass
class Album:
    uri: str
    name: str


@dataclass
class Artist:
    uri: str
    name: str


@dataclass
class Track:
    uri: str
    name: str

    explicit: bool

    album: Album
    artists: List[Artist]

    @classmethod
    def from_response(cls, response):
        album = Album(
            response['album']['uri'],
            response['album']['name'],
        )

        artists = [
            Artist(
                artist_response['uri'],
                artist_response['name'],
            )
            for artist_response in response['artists']
        ]

        return cls(
            response['uri'],
            response['name'],
            response['explicit'],
            album,
            artists,
        )

    @property
    def search_query(self):
        artist_names = (artist.name for artist in self.artists)
        artist_query = " ".join(artist_names)

        return f"{self.name} {self.album.name} {artist_query}"
