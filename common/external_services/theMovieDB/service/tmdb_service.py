# -*- coding: utf-8 -*-
import pprint

from common.external_services.theMovieDB.core.tmdb_tvshow_api import TmdbTvShowApi
from common.external_services.theMovieDB.core.tmdb_movie_api import TmdbMovieApi
from common.external_services.theMovieDB.core.models.movie_nowplaying import (
    NowPlayingByCountry,
)


class TmdbService:

    def __init__(self):
        self.movie_api = TmdbMovieApi()
        self.tv_show_api = TmdbTvShowApi()

    # The latest in country
    def latest_movie_by_country(self, country_code: str) -> list:
        """
        Retrieve the latest movies currently playing in a specific country.

        Fetches movies that are currently playing, retrieves their latest release information,
        and filters by the given country code. Returns a list of `MovieByCountry` instances.

        Parameters:
            country_code (str): ISO 3166-1  country code (e.g., 'IT').

        Returns:
            list: List of `MovieByCountry` instances for the specified country.
        """

        # Get every the movie now_playing
        now_playing = self.movie_api.now_playing()
        for movie in now_playing:
            # For each movie get each latest
            latest_movie_list = self.movie_api.latest_movie(now_playing=movie)

            # For each latest search for the preferred country code
            return [
                NowPlayingByCountry.create(now_playing=movie, release_info=release_info)
                for release_info in latest_movie_list
                if release_info.iso_3166_1 == country_code
            ]

    def latest_show_by_country(self, country_code: str) -> list:
        """
        Retrieve the latest TV shows from a specific country

        Parameters:
            country_code (str): The ISO 3166-1 alpha-2 country code (e.g., 'IT' for Italy)

        Returns:
            list: A list of TvShowByCountry instances for TV shows from the specified country
        """
        # Get each tv_show by country
        """
        return [
            TvShowByCountry.create(tvshow=tv_show)
            for tv_show in self.tv_show_api.  .on_the_air()
            if tv_show.origin_country == country_code
        ]
        """

    def tv_show(self):
        results = self.tv_show_api.tv_show_translations(tv_show_id=57532)
        pprint.pprint(results)

