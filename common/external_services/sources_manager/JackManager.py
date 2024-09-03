# -*- coding: utf-8 -*-

from common.external_services.theMovieDB.country import TvShowByCountry
from common.external_services.theMovieDB.tmdb import Tmdb
from common.external_services.theMovieDB.response import NowPlayingByCountry


class JackManager:

    def __init__(self):
        self.tmdb = Tmdb()

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
        now_playing = self.tmdb.get_now_playing()
        for movie in now_playing:

            # For each movie get each latest
            latest_movie_list = self.tmdb.get_latest_movie(now_playing=movie)

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
        return [
            TvShowByCountry.create(tvshow=tv_show)
            for tv_show in self.tmdb.get_tv_show()
            if tv_show.origin_country == country_code
        ]
