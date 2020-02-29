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

    def __hash__(self):
        return hash(self.id)


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

    def is_appropriate_variant_of(self, other):
        return (
            self.name == other.name
            and self.album.name == other.album.name
            and set(self.artists) == set(other.artists)
        )

    def __hash__(self):
        return hash(self.id)


@dataclass
class Playlist:
    id: str
    name: str
    owner_id: str

    collaborative: bool
    public: bool

    @classmethod
    def from_response(cls, response):
        return cls(
            id=response["id"],
            name=response["name"],
            owner_id=response["owner"]["id"],
            collaborative=response["collaborative"],
            public=response["public"],
        )
