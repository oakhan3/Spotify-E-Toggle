from dataclasses import dataclass
from typing import List


@dataclass
class Album:
    id: str
    name: str


@dataclass
class Artist:
    id: str
    name: str


@dataclass
class Track:
    id: str
    name: str

    explicit: bool

    album: Album
    artists: List[Artist]

    @classmethod
    def from_response(cls, response):
        album = Album(response["album"]["id"], response["album"]["name"])

        artists = [
            Artist(artist_response["id"], artist_response["name"])
            for artist_response in response["artists"]
        ]

        return cls(response["id"], response["name"], response["explicit"], album, artists)

    @property
    def search_query(self):
        artist_names = (artist.name for artist in self.artists)
        artist_query = " ".join(artist_names)

        return f"{self.name} {self.album.name} {artist_query}"

    def __hash__(self):
        return hash(self.id)
