# -*- coding: utf-8 -*-

from typing import TypeVar

from common.external_services.theMovieDB.core.models.tvshow.alternative import Alternative
from common.external_services.theMovieDB.core.models.movie.nowplaying import NowPlaying
from common.external_services.theMovieDB.core.models.tvshow.on_the_air import OnTheAir
from common.external_services.theMovieDB.core.models.tvshow.tvshow import TvShow
from common.external_services.theMovieDB.core.models.movie.movie import Movie
from common.external_services.theMovieDB.core.videos import Videos
from common.external_services.theMovieDB.core.keywords import Keyword
from common.external_services.mediaresult import MediaResult
from common.external_services.sessions.session import MyHttp
from common.external_services.trailers.api import YtTrailer
from common.external_services.sessions.agents import Agent
from common.external_services.theMovieDB import config
from common.external_services.imdb import IMDB
from common.utility import ManageTitles
from view import custom_console


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

    # Content -> search response attribute
    show = {
        1: "movie",
        2: "tv",
    }

    def __init__(self):
        """
        Initialize the Api instance with an HTTP client
        """
        headers = Agent.headers()
        super().__init__(headers)
        self.http_client = self.session

    def _search(self, query: str, category: int) -> list[T] | None:
        """
        Searches for data based on a query and category.
        :param query: search query
        :param category: category of the search query, e.g., 'movie' or 'tv'
        :return: list of T or None
        """
        # Only tv and movie
        if category > 2:
            custom_console.bot_warning_log("Check the category of the search query")
            return []
        if endpoint_class:=self.ENDPOINTS.get(TmdbAPI.show[category]):
            request = endpoint_class.search(query)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []

    def nowplaying(self, category: int) -> list[T] | None:
        """
        Searches for now playing content based on a query and category.
        :param query: query for now playing
        :param category: category of the now playing content, e.g., 'movie' or 'tv'
        :return: list of T or None
        """

        if endpoint_class:=self.ENDPOINTS.get(TmdbAPI.show[category]):
            request = endpoint_class.playing()
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []

    def alternative(self, media_id: int, category: int) -> list[T] | None:
        """
        Searches for data based on a query and category.
        :param media_id: id of the media to search for
        :param category: category of the search query, e.g., 'movie' or 'tv'
        :return: list of T or None
        """
        if endpoint_class:=self.ENDPOINTS.get(TmdbAPI.show[category]):
            request = endpoint_class.alternative(media_id)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []

    def _videos(self, video_id: int, category: int) -> list[T] | None:
        if endpoint_class:=self.ENDPOINTS.get(TmdbAPI.show[category]):
            request = endpoint_class.videos(video_id)
            return self.request(endpoint=request)
        else:
            print(f"Endpoint for category '{category}' not found.")
            return []


    def _keywords(self, video_id: int, category: int) -> list[T] | None:
        if endpoint_class:=self.ENDPOINTS.get(TmdbAPI.show[category]):
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
                response_data = response.json().get(endpoint['results'], [])
                return [endpoint['datatype'](**attribute) for attribute in response_data]
            else:
                return []


class DbOnline(TmdbAPI):
    def __init__(self, query: str, category: int) -> None:
        super().__init__()
        self.query = query
        self.category = category
        self.media_result = self.search()

    def search(self) -> MediaResult | None:
        """
        """
        results = self._search(self.query, self.category)
        # User imdb_id when tmdb_id is not available
        imdb_id = 0
        if results:
            for result in results:
                if ManageTitles.fuzzyit(str1=self.query, str2=result.get_title()) > 95:
                    # Get the trailer
                    trailer_key = self.trailer(result.id)
                    keywords_list = self.keywords(result.id)
                    # return MediaResult object
                    search_results = MediaResult(result, video_id=result.id,imdb_id=imdb_id, trailer_key=trailer_key,
                                                 keywords_list=keywords_list)
                    self.print_results(results=search_results)
                    return search_results

        # not results found so try to initialize imdb
        imdb = IMDB()
        user_tmdb_id  = custom_console.user_input(message="Title not found. Please digit a valid TMDB ID ->")

        # Try to add IMDB ID if tmdb is not available
        if user_tmdb_id==0:
            imdb_id = imdb.search(query=self.query)
            trailer_key = None
            keywords_list = []
        else:
            # Request trailer and keywords
            trailer_key = self.trailer(user_tmdb_id)
            keywords_list = self.keywords(user_tmdb_id) if trailer_key else ''

        search_results = MediaResult(video_id=user_tmdb_id, imdb_id=imdb_id, trailer_key=trailer_key, keywords_list=keywords_list)
        self.print_results(results=search_results)
        return search_results

    def youtube_trailer(self) -> str | None:
        # Search trailer on YouTube
        custom_console.bot_question_log("TMDB trailer not found. Try searching on YouTube...\n")

        yt_trailer = YtTrailer(self.query)
        result = yt_trailer.get_trailer_link()
        if result:
            custom_console.bot_question_log("Found !\n")
            # choose the first in the list
            # todo compare against the media title especially for the favorite channel
            return result[0].items[0].id.videoId


    def trailer(self, video_id: int) -> str | None:
        trailers = self._videos(video_id, self.category)

        # Invalid video_id or video_id not found
        if not trailers:
            return None

        trailer = next(
            (video for video in trailers if video.type.lower() == 'trailer' and video.site.lower() == 'youtube'), None)
        if trailer:
            return trailer.key
        return self.youtube_trailer()

    def keywords(self, video_id: int) -> str | None:
        keywords_list = self._keywords(video_id, self.category)
        if keywords_list:
            return ",".join([key.name for key in keywords_list])


    def print_results(self,results: MediaResult) -> None:
            custom_console.bot_log(f"'TMDB TITLE'..... {self.query}")
            custom_console.bot_log(f"'TMDB ID'........ {results.video_id}")
            custom_console.bot_log(f"'TMDB KEYWORDS'.. {results.keywords_list}")
            print()