# -*- coding: utf-8 -*-

from common.external_services.theMovieDB.response import MovieReleaseInfo, NowPlaying, TvShow


class MovieByCountry:

    def __init__(self, movie: NowPlaying, release_info: MovieReleaseInfo):
        self.movie = movie
        self.release_info = release_info

    @classmethod
    def create(cls, movie: NowPlaying, release_info: MovieReleaseInfo):
        return cls(movie=movie, release_info=release_info)

    def __repr__(self):
        """Returns a string representation"""
        return f"<Movie={self.movie}, release_info={self.release_info}>"


class TvShowByCountry:

    def __init__(self, tvshow: TvShow):
        self.tvshow = tvshow

    @classmethod
    def create(cls, tvshow: TvShow):
        return cls(tvshow=tvshow)

    def __repr__(self):
        """Returns a string representation"""
        return f"<TvShow={self.tvshow}>"
