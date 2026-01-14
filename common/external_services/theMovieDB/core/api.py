# -*- coding: utf-8 -*-
import os
import hashlib
from datetime import datetime

import diskcache
from typing import TypeVar

from common.external_services.theMovieDB.core.models.tvshow.alternative import Alternative
from common.external_services.theMovieDB.core.models.tvshow.details import TVShowDetails
from common.external_services.theMovieDB.core.models.movie.details import MovieDetails
from common.external_services.theMovieDB.core.models.movie.nowplaying import NowPlaying
from common.external_services.theMovieDB.core.models.tvshow.on_the_air import OnTheAir
from common.external_services.theMovieDB.core.models.tvshow.tvshow import TvShow
from common.external_services.theMovieDB.core.models.movie.movie import Movie
from common.external_services.theMovieDB.core.keywords import Keyword
from common.external_services.theMovieDB.core.videos import Videos
from common.external_services.mediaresult import MediaResult
from common.external_services.sessions.session import MyHttp
from common.external_services.trailers.api import YtTrailer
from common.external_services.sessions.agents import Agent
from common.external_services.theMovieDB import config
from common.external_services.imdb import IMDB
from common.utility import ManageTitles

from unit3dup.media import Media
from view import custom_console


from unit3dup import config_settings

base_url = "https://api.themoviedb.org/3"
ENABLE_LOG = True
T = TypeVar('T')

class MovieEndpoint:
    @staticmethod
    def search(query: str)-> dict:
        return {'url': f'{base_url}/search/movie', 'datatype': Movie, 'query': query, 'results': 'results' }


    @staticmethod
    def playing()-> dict:
        return {'url': f'{base_url}/movie/now_playing', 'datatype': NowPlaying, 'query': '', 'results': 'results'}


    @staticmethod
    def alternative(movie_id: int)-> dict:
        return {'url': f'{base_url}/movie/{movie_id}/alternative_titles', 'datatype': Alternative, 'query': '',
                'results': 'titles'}


    @staticmethod
    def videos(movie_id: int)-> dict:
        return {'url': f'{base_url}/movie/{movie_id}/videos', 'datatype': Videos, 'query': '',
                'results': 'results'}

    @staticmethod
    def details(movie_id: int)-> dict:
        return {'url': f'{base_url}/movie/{movie_id}', 'datatype': MovieDetails, 'query': ''}


    @staticmethod
    def keywords(movie_id: int)-> dict:
        return {'url': f'{base_url}/movie/{movie_id}/keywords', 'datatype': Keyword, 'query': '',
                'results': 'keywords'}


class TvEndpoint:
    @staticmethod
    def search(query: str):
        return {'url': f'{base_url}/search/tv', 'datatype': TvShow, 'query': query, 'results': 'results'}


    @staticmethod
    def playing():
        return {'url': f'{base_url}/tv/on_the_air', 'datatype': OnTheAir, 'query': '', 'results': 'results'}


    @staticmethod
    def alternative(serie_id: int) -> dict:
        return {'url': f'{base_url}/tv/{serie_id}/alternative_titles', 'datatype': Alternative, 'query': '',
                'results': 'results'}


    @staticmethod
    def videos(serie_id: int)-> dict:
        return {'url': f'{base_url}/tv/{serie_id}/videos', 'datatype': Videos, 'query': '',
                'results': 'results'}

    @staticmethod
    def details(serie_id: int)-> dict:
        return {'url': f'{base_url}/tv/{serie_id}', 'datatype': TVShowDetails, 'query': ''}



    @staticmethod
    def keywords(serie_id: int)-> dict:
        return {'url': f'{base_url}/tv/{serie_id}/keywords', 'datatype': Keyword, 'query': '',
                'results': 'results'}



class TmdbAPI(MyHttp):

    params = {
        "api_key": config.TMDB_APIKEY,
        "language": "it-IT",
    }

    # Mappatura automatica degli endpoint
    ENDPOINTS = {
        'movie': MovieEndpoint,
        'tv': TvEndpoint,
    }

    def __init__(self):
        """
        Initialize the Api instance with an HTTP client
        """
        headers = Agent.headers()
        super().__init__(headers)
        self.http_client = self.session

    def _search(self, query: str, category: str) -> list[T] | None:
        """
        Searches for data based on a query and category.
        :param query: search query
        :param category: category of the search query, e.g., 'movie' or 'tv'
        :return: list of T or None
        """
        # Only tv and movie
        if category not in ['movie', 'tv']:
            custom_console.bot_warning_log("Check the category of the search query")
            return []
        if endpoint_class := self.ENDPOINTS.get(category):
            request = endpoint_class.search(query)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []

    def nowplaying(self, category: str) -> list[T] | None:
        """
        Searches for now playing content based on a query and category.
        :param category: category of the now playing content, e.g., 'movie' or 'tv'
        :return: list of T or None
        """

        if endpoint_class:=self.ENDPOINTS.get(category):
            request = endpoint_class.playing()
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []

    def alternative(self, media_id: int, category: str) -> list[T] | None:
        """
        Searches for data based on a query and category.
        :param media_id: id of the media to search for
        :param category: category of the search query, e.g., 'movie' or 'tv'
        :return: list of T or None
        """
        if endpoint_class:=self.ENDPOINTS.get(category):
            request = endpoint_class.alternative(media_id)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []

    def _videos(self, video_id: int, category: str) -> list[T] | None:
        if endpoint_class:=self.ENDPOINTS.get(category):
            request = endpoint_class.videos(video_id)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []

    def details(self, video_id: int, category: str) -> list[T] | None:
        if endpoint_class:=self.ENDPOINTS.get(category):
            request = endpoint_class.details(video_id)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []


    def _keywords(self, video_id: int, category: str) -> list[T] | None:
        if endpoint_class:=self.ENDPOINTS.get(category):
            request = endpoint_class.keywords(video_id)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []


    def request(self, endpoint: dict) -> list[T] | None:
        """
        Sends a request to the API and returns a list of instances of the specified 'datatype'.
        :param endpoint: request endpoint
        :return: list of T or None
        """
        params = {**TmdbAPI.params, "query": endpoint['query']}
        response = self.get_url(endpoint['url'], params=params)

        if response:
            if response.status_code == 200:
                if not endpoint.get('results', None):
                    response_data = [response.json()]
                else:
                    response_data = response.json().get(endpoint['results'], [])

                return [endpoint['datatype'](**attribute) for attribute in response_data]
            else:
                return []
        return None

class DbOnline(TmdbAPI):
    def __init__(self, media: Media, category: str, no_title: str) -> None:
        super().__init__()
        self.media = media
        self.query = media.guess_title
        self.category = category

        # Load the cache file
        if config_settings.user_preferences.CACHE_DBONLINE:
            self.cache = diskcache.Cache(str(os.path.join(config_settings.user_preferences.CACHE_PATH, "tmdb.cache")))

        if media.tmdb_id or media.imdb_id:
            # Skip cache if there is a tmdb id or imdb in the title string
            self.media_result = self. results_in_string(tmdb_id=int(media.tmdb_id), imdb_id=int(media.imdb_id))
        else:
            # Load from the cache or search online for a tmdb id or imdb
            # Search for a video based on the filename or the title from the -notitle flag in the CLI
            if no_title:
                self.query = no_title
            self.media_result = self.search()

    @staticmethod
    def hash_key(key: str) -> str:
        """ Generate a hashkey for the cache index """
        return hashlib.md5(key.encode('utf-8')).hexdigest()

    def is_like(self, results: list[T]) -> T | bool:
        if results:
            # Search for in the tile or original_name
            for result in results:
                # check date
                if result.get_date() and self.media.guess_filename.guessit_year:
                    if not datetime.strptime(result.get_date(), '%Y-%m-%d').year == self.media.guess_filename.guessit_year:
                       continue

                # Search for title
                if ManageTitles.fuzzyit(str1=self.query, str2=ManageTitles.clean_text(result.get_title())) > 95:
                    return result

                if ManageTitles.fuzzyit(str1=self.query, str2=ManageTitles.clean_text(result.get_original())) > 95:
                    return result

            # Search for alternative title
            for result in results:
                alternative = self.alternative(media_id=result.id, category=self.category)
                for alt in alternative:
                    if ManageTitles.fuzzyit(str1=self.query, str2=alt.title) > 95:
                        return result
        return False

    def results_in_string(self, tmdb_id:int, imdb_id:int)-> MediaResult:
        """
        Use id from the string filename or name folder
        Cache disabled
        """
        keywords_list = ''
        trailer_key = ''

        if tmdb_id:
            if tmdb_id > 0:
                # Request trailer and keywords
                trailer_key = self.trailer(tmdb_id)
                keywords_list = self.keywords(tmdb_id) if trailer_key else ''
        else:
            tmdb_id = 0

        search_results = MediaResult(video_id=tmdb_id, imdb_id=imdb_id, trailer_key=trailer_key,
                                     keywords_list=keywords_list)
        self.print_results(results=search_results)
        return search_results


    def search(self) -> MediaResult | None:
        """
        Search for results based on a tmdb query
        season: True = search for a season. Title unknown
        """

        # Search in the cache first if cache is enabled
        if config_settings.user_preferences.CACHE_DBONLINE:
            search_results = self.load_cache(self.hash_key(self.query))
            if search_results:
                self.print_results(results=search_results)
                return search_results

        # or start an on-line search
        results = self._search(self.query, self.category)
        # Use imdb_id when tmdb_id is not available
        imdb_id = 0
        if results:
            if result:=self.is_like(results):
                # Get the trailer
                trailer_key = self.trailer(result.id)
                keywords_list = self.keywords(result.id)
                search_results = MediaResult(result, video_id=result.id, imdb_id=imdb_id,
                                             trailer_key=trailer_key, keywords_list=keywords_list)

                self.print_results(results=search_results)
                # Write to the cache if it is enabled
                if config_settings.user_preferences.CACHE_DBONLINE:
                    self.cache[self.hash_key(self.query)] = search_results
                # return the result
                return search_results

        # No response from TMDB
        if results is None:
            custom_console.bot_error_log(
                f"TMDB - No response from the remote host or the API key is invalid. Retry or update your key")
            exit(1)

        # not results found so try to initialize imdb
        custom_console.bot_warning_log(f"Title not found.What the bot has understood:")

        custom_console.bot_warning_log(f"Title:   '{self.query}'\ncategory:'{self.category}'")
        if self.category in 'tv':
            serie = f"S{str(self.media.guess_season).zfill(2)}" if self.media.guess_season else ''
            if not self.media.torrent_pack:
                serie += f"E{str(self.media.guess_episode).zfill(2)}"
            custom_console.bot_warning_log(f"details: '{serie}' Pack: '{self.media.torrent_pack}'")

        # Ask User TMDB ID
        search_results = self.manual_search()
        self.cache[self.hash_key(self.query)] = search_results
        return search_results


    def manual_search(self) -> MediaResult | None:
        """
                 User digits valid TMDB id or wait
                 User digits 0 if he wants to search on IMDB
                 Returns:
                     MediaResult
        """
        imdb = IMDB()
        imdb_id = 0
        user_id = 0
        while True:
            # Check if user wants to skip
            if not config_settings.user_preferences.SKIP_TMDB:
                try:
                    user_id = custom_console.user_input(message=f"Please digit a valid TMDB ID (0=skip)->")
                except KeyboardInterrupt:
                    custom_console.bot_error_log("\nOperation cancelled")
                    exit(0)
            else:
                custom_console.bot_warning_log(f"\n ** Auto skip TMDB ID **\n")

            # Try to add IMDB ID if tmdb is not available
            if user_id==0:
                imdb_id = imdb.search(query=self.query)
                # try searching for a YouTube video anyway
                trailer_key = self.youtube_trailer()
                search_results = MediaResult(video_id=user_id, imdb_id=imdb_id, trailer_key=trailer_key,
                                             keywords_list='not available')
                self.print_results(results=search_results)
                return search_results
            else:
                result = self.search_id(video_id=user_id)
                if result:
                    # Request trailer and keywords
                    trailer_key = self.trailer(user_id)
                    keywords_list = self.keywords(user_id) if trailer_key else ''
                    search_results = MediaResult(result=result, video_id=user_id, imdb_id=imdb_id, trailer_key=trailer_key,
                                                 keywords_list=keywords_list)
                    self.print_results(results=search_results)
                    return search_results


    def youtube_trailer(self) -> str | None:
        # Search trailer on YouTube
        if 'no_key'  in config_settings.tracker_config.YOUTUBE_KEY:
            return "not available"

        yt_trailer = YtTrailer(self.query)
        result = yt_trailer.get_trailer_link()
        if result:
            # choose the first in the list
            # todo compare against the media title especially for the favorite channel
            return result[0].items[0].id.videoId
        else:
            if not config_settings.user_preferences.SKIP_YOUTUBE:
                user_youtube_id = custom_console.user_input_str(message="Title not found."
                                                                        " Please digit a valid Youtube ID (0=skip)->")
                if user_youtube_id==0:
                    return "not available"
                return user_youtube_id
            return None

    def trailer(self, video_id: int) -> str | None:
        # Search for tmdb trailer
        trailers = self._videos(video_id, self.category)
        if trailers:
            trailer = next((video for video in trailers if video.type.lower() == 'trailer'
                            and video.site.lower() == 'youtube'), None)
            if trailer:
                return trailer.key
            else:
                return "not available"

        # Search for YouTube trailer
        return self.youtube_trailer()

    def keywords(self, video_id: int) -> str | None:
        keywords_list = self._keywords(video_id, self.category)
        if keywords_list:
            return ",".join([key.name for key in keywords_list])
        else:
            return "not available"


    def print_results(self,results: MediaResult) -> None:
            custom_console.bot_log(f"'TMDB TITLE'..... {self.query}")
            custom_console.bot_log(f"'TMDB ID'........ {results.video_id}")
            if results.imdb_id:
                custom_console.bot_warning_log(f"_'IMDB ID'_........ '{results.imdb_id}'")
            custom_console.bot_log(f"'TMDB KEYWORDS'.. {results.keywords_list}")
            custom_console.bot_log(f"'TRAILER CODE' .. {results.trailer_key}")


    def load_cache(self, query: str)-> MediaResult | None:
        # Check if the item is in the cache
        if query not in self.cache:
            return None

        custom_console.bot_warning_log(f"<> Using cached results")
        try:
            # Try to get the video from the cache
            return self.cache[query]
        except KeyError:
            # Handle the case where the video is missing or the cache is corrupted
            custom_console.bot_error_log("Cached frame not found or cache file corrupted")
            custom_console.bot_error_log("Proceed to extract the screenshot again. Please wait..")
            return None


    def search_id(self, video_id: int) -> list[T] | None:
        """
                 Search Movie or Tvshow based on ID
                 Build a DataClass for the MediaResult
                 Returns:
                     list[T]: generic Movie or Tvshow results
        """
        result = self.details(video_id=video_id, category=self.category)
        if result:
            return result[0]
        return None