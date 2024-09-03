# -*- coding: utf-8 -*-
from abc import ABC


class TmdbResponse(ABC):
    """
    TMDB response object base class
    """

    def __repr__(self):
        """
        Abstract method for returning a string representation of the instance.
        Must be implemented by subclasses.
        """
        pass


class NowPlaying(TmdbResponse):
    """
    Represents a movie with various attributes.
    """

    def __init__(
        self,
        adult=None,
        backdrop_path=None,
        genre_ids=None,
        id=None,
        original_language=None,
        original_title=None,
        overview=None,
        popularity=None,
        poster_path=None,
        release_date=None,
        title=None,
        video=None,
        vote_average=None,
        vote_count=None,
    ):
        """
        Initializes a Movie instance with provided attributes.
        """
        self.adult = adult
        self.backdrop_path = backdrop_path
        self.genre_ids = genre_ids
        self.id = id
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.poster_path = poster_path
        self.release_date = release_date
        self.title = title
        self.video = video
        self.vote_average = vote_average
        self.vote_count = vote_count

    def __repr__(self):
        """Returns a string representation"""
        return f"<Movie title={self.title} id={self.id}>"

    @classmethod
    def release_info(cls, iso_3166_1=None, release_dates=None):
        """
        Initializes a ReleaseInfo instance with provided attributes.
        """
        return cls(iso_3166_1, release_dates)


class MovieReleaseInfo(TmdbResponse):
    """
    Represents release information for a movie in a specific country.
    """

    def __init__(self, iso_3166_1=None, release_dates=None):
        """
        Initializes a ReleaseInfo instance with provided attributes.
        """
        self.iso_3166_1 = iso_3166_1
        self.release_dates = release_dates

    def __repr__(self):
        """Returns a string representation"""
        return f"<ReleaseInfo iso_3166_1={self.iso_3166_1}, release_dates={self.release_dates}>"


class NowPlayingByCountry(TmdbResponse):
    """
    Represents a combined movie object with attributes from both NowPlaying and MovieReleaseInfo.
    """

    def __init__(
        self,
        adult=None,
        backdrop_path=None,
        genre_ids=None,
        id=None,
        original_language=None,
        original_title=None,
        overview=None,
        popularity=None,
        poster_path=None,
        release_date=None,
        title=None,
        video=None,
        vote_average=None,
        vote_count=None,
        iso_3166_1=None,
        release_dates=None,
    ):
        """
        Initializes a CombinedMovieInfo instance with attributes from both NowPlaying and MovieReleaseInfo.
        """
        # Attributes from NowPlaying
        self.adult = adult
        self.backdrop_path = backdrop_path
        self.genre_ids = genre_ids
        self.id = id
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.poster_path = poster_path
        self.release_date = release_date
        self.title = title
        self.video = video
        self.vote_average = vote_average
        self.vote_count = vote_count

        # Attributes from MovieReleaseInfo
        self.iso_3166_1 = iso_3166_1
        self.release_dates = release_dates

    def __repr__(self):
        """Returns a string representation"""
        return (
            f"<NowPlayingByCountry title={self.title} id={self.id}, "
            f"iso_3166_1={self.iso_3166_1}, release_dates={self.release_dates}>"
        )

    @classmethod
    def create(cls, now_playing, release_info):
        """
        Creates a CombinedMovieInfo instance from NowPlaying and MovieReleaseInfo instances.

        Parameters:
            now_playing (NowPlaying): An instance of the NowPlaying class.
            release_info (MovieReleaseInfo): An instance of the MovieReleaseInfo class.

        Returns:
            CombinedMovieInfo: A new instance combining attributes from both classes.
        """
        return cls(
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


class TvShow(TmdbResponse):
    """
    Represents a TV show with various attributes.
    """

    def __init__(
        self,
        adult=None,
        backdrop_path=None,
        genre_ids=None,
        id=None,
        original_language=None,
        original_title=None,
        overview=None,
        popularity=None,
        poster_path=None,
        release_date=None,
        title=None,
        video=None,
        vote_average=None,
        vote_count=None,
        origin_country=None,
        original_name=None,
        first_air_date=None,
        name=None,
    ):
        """
        Initializes a TvShow instance with provided attributes.
        """
        self.adult = adult
        self.backdrop_path = backdrop_path
        self.genre_ids = genre_ids
        self.id = id
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.poster_path = poster_path
        self.release_date = release_date
        self.title = title
        self.video = video
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.origin_country = origin_country
        self.original_name = original_name
        self.first_air_date = first_air_date
        self.name = name

    def __repr__(self):
        """Returns a string representation"""
        return f"<TvShow title={self.name} id={self.id}>"
