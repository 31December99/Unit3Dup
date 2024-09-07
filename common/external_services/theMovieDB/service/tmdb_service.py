# -*- coding: utf-8 -*-
import pprint

from common.external_services.theMovieDB.core.tvshow_api import TmdbTvShowApi
from common.external_services.theMovieDB.core.movie_api import TmdbMovieApi
from common.external_services.theMovieDB.core.models.tvshow.on_the_air import OnTheAir
from common.external_services.theMovieDB.core.models.movie.nowplaying import (
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

        # Get all the movies currently playing
        now_playing = self.movie_api.now_playing()

        results = []

        for movie in now_playing:
            # For each movie, get its latest release information
            latest_movie_list = self.movie_api.latest_movie(now_playing=movie)

            # Filter the releases by the preferred country code and create NowPlayingByCountry instances
            country_movies = [
                NowPlayingByCountry.from_data(now_playing=movie, release_info=release_info)
                for release_info in latest_movie_list
                if release_info.iso_3166_1 == country_code
            ]

            # Add the filtered movies to the results list
            results.extend(country_movies)

        return results

    def movie_alternative_title(self, movie_id: int):
        return self.movie_api.movie_alternative_title(movie_id=movie_id)

    def search_movies(self, query: str):
        return self.movie_api.search_movies(query=query)

    def latest_show_by_country(self, country_code: str) -> list["OnTheAir"]:
        """
        Retrieve the latest TV shows from a specific country

        Parameters:
            country_code (str): The ISO 3166-1 alpha-2 country code (e.g., 'IT' for Italy)

        Returns:
            list: A list of OnTheAir instances for TV shows from the specified country
        """
        # Get each tv_show by country
        on_the_air_list = self.tv_show_api.on_the_air()

        filtered_shows = []

        for on_the_air in on_the_air_list:
            # Query all translations for the TV show
            tv_show_list = self.tv_show_api.tv_show_translations(
                tv_show_id=on_the_air.id
            )

            # Get the languages from the translations
            translation_languages = {
                translation.iso_639_1.lower()
                for translation in tv_show_list.translations
            }

            # Check if the preferred language is available
            if country_code.lower() in translation_languages:
                filtered_shows.append(on_the_air)
        return filtered_shows

    def tv_show_details(self, tv_show_id):
        return self.tv_show_api.tv_show_details(tv_show_id=tv_show_id)

    def search_tv_show(self, query: str):
        return self.tv_show_api.search_tv_shows(query=query)

