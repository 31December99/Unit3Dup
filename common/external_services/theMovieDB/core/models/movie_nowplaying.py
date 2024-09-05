# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from .movie_release_info import MovieReleaseInfo


@dataclass
class NowPlaying:
    """
    Represents a movie with various attributes.
    """

    adult: bool | None = None
    backdrop_path: str | None = None
    genre_ids: list[int] = field(default_factory=list)
    id: int | None = None
    original_language: str | None = None
    original_title: str | None = None
    overview: str | None = None
    popularity: float | None = None
    poster_path: str | None = None
    release_date: str | None = None
    title: str | None = None
    video: bool | None = None
    vote_average: float | None = None
    vote_count: int | None = None

    def __repr__(self):
        """Returns a string representation"""
        return f"<Movie title={self.title} id={self.id}>"


@dataclass
class NowPlayingByCountry:
    """
    Represents a combined movie object with attributes from both NowPlaying and MovieReleaseInfo.
    """

    adult: bool | None = None
    backdrop_path: str | None = None
    genre_ids: list[int] = field(default_factory=list)
    id: int | None = None
    original_language: str | None = None
    original_title: str | None = None
    overview: str | None = None
    popularity: float | None = None
    poster_path: str | None = None
    release_date: str | None = None
    title: str | None = None
    video: bool | None = None
    vote_average: float | None = None
    vote_count: int | None = None
    iso_3166_1: str | None = None
    release_dates: dict[str, str] = field(default_factory=dict)

    def __repr__(self):
        """Returns a string representation"""
        return (
            f"<NowPlayingByCountry title={self.title} id={self.id}, "
            f"iso_3166_1={self.iso_3166_1}, release_dates={self.release_dates}>"
        )

    @staticmethod
    def create(
            now_playing: NowPlaying, release_info: "MovieReleaseInfo"
    ) -> "NowPlayingByCountry":
        """
        Creates a NowPlayingByCountry instance from NowPlaying and MovieReleaseInfo instances.

        Parameters:
            now_playing (NowPlaying): An instance of the NowPlaying class.
            release_info (MovieReleaseInfo): An instance of the MovieReleaseInfo class.

        Returns:
            NowPlayingByCountry: A new instance combining attributes from both classes.
        """
        return NowPlayingByCountry(
            adult=now_playing.adult,
            backdrop_path=now_playing.backdrop_path,
            genre_ids=now_playing.genre_ids,
            id=now_playing.id,
            original_language=now_playing.original_language,
            original_title=now_playing.original_title,
            overview=now_playing.overview,
            popularity=now_playing.popularity,
            poster_path=now_playing.poster_path,
            release_date=now_playing.release_date,
            title=now_playing.title,
            video=now_playing.video,
            vote_average=now_playing.vote_average,
            vote_count=now_playing.vote_count,
            iso_3166_1=release_info.iso_3166_1,
            release_dates=release_info.release_dates,
        )
