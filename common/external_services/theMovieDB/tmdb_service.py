# -*- coding: utf-8 -*-

from common.external_services.theMovieDB.core.models.movie.nowplaying import  NowPlayingByCountry
from common.external_services.theMovieDB.core.models.tvshow.on_the_air import OnTheAir
from common.external_services.theMovieDB.core.models.multi import Movie,TVShow
from common.external_services.theMovieDB.core.tvshow_api import TmdbTvShowApi
from common.external_services.theMovieDB.core.movie_api import TmdbMovieApi
from common.external_services.theMovieDB.core.multi_api import TmdbMultiApi
from common.external_services.trailers.api import YtTrailer
from common.custom_console import custom_console
from common.utility.utility import ManageTitles
from unit3dup.contents import Contents



class TmdbService:

    def __init__(self):
        self.movie_api = TmdbMovieApi()
        self.tv_show_api = TmdbTvShowApi()
        self.multi_api = TmdbMultiApi()

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

    def keywords(self, title: str, video_id: int, category: str) -> str | None:
        keywords  = self.multi_api.keywords(query=title, video_id=video_id, category=category)

        keywords_list = []
        if category == "movie":
         keywords_list = keywords.get("keywords", [])

        if category == "serie":
         keywords_list = keywords.get("results", [])

        if keywords_list:
           return ",".join([key["name"] for key in keywords_list])


    def search(self, query: Contents)-> Movie | TVShow | None:

        # Content -> search response attribute
        show = {
            1: "movie",
            2: "tv",
        }

        # TMDB Multi request
        results = self.multi_api.multi(query=query.guess_title, category = query.category)

        # Based on category , compare query title with result title
        for result in results:
            if ManageTitles.fuzzyit(str1=result.get_title(), str2=query.guess_title) > 95:

                # Search the trailer code
                result.trailer_code = self.trailer(title=query.guess_title, video_id=result.get_id(),
                                            category=show[query.category])

                result.keywords = self.keywords(title=query.guess_title, video_id=result.get_id(),
                                             category=show[query.category])
                return result


        #input("Press Enter to continue... NON TROVATO")



    def trailer(self, title: str, video_id: int, category: str)-> str | None:
        # Query videos endpoint
        videos = self.multi_api.videos(query=title, video_id=video_id, category=category)

        # Get the youtube trailer code from the result if it exists
        trailer = next((video for video in videos['results'] if video['type'].lower() == 'trailer'
                        and video['site'].lower() == 'youtube'), None)
        if trailer:
            return trailer['key']
        else:
            return self.youtube_trailer(query=title)

    @staticmethod
    def youtube_trailer(query: str):

        # Search trailer on youtube
        custom_console.bot_question_log("TMDB trailer not found. Try searching on YouTube...\n")

        yt_trailer = YtTrailer(query)
        result = yt_trailer.get_trailer_link()
        if result:
            custom_console.bot_question_log("Found !\n")
            # choose the first in the list
            # todo compare against the media title especially for the favorite channel
            return result[0].items[0].id.videoId



