# -*- coding: utf-8 -*-

import os
import hashlib
from datetime import datetime
from typing import TypeVar

import diskcache

from unit3dup.external.movie_db.models.tvshow.alternative import Alternative
from unit3dup.external.movie_db.models.tvshow.translations import (
    Translation as TvTranslation,
)
from unit3dup.external.movie_db.models.movie.translations import (
    Translation as MovieTranslation,
)
from unit3dup.external.movie_db.models.tvshow.details import TVShowDetails
from unit3dup.external.movie_db.models.movie.details import MovieDetails
from unit3dup.external.movie_db.models.movie.nowplaying import NowPlaying
from unit3dup.external.movie_db.models.tvshow.on_the_air import OnTheAir
from unit3dup.external.movie_db.models.tvshow.tvshow import TvShow
from unit3dup.external.movie_db.models.movie.movie import Movie
from unit3dup.external.movie_db.models.keywords import Keyword
from unit3dup.external.movie_db.models.videos import Videos
from unit3dup.external.movie_db.mediaresult import MediaResult

from unit3dup.external.agents import Agent
from unit3dup.external.http_client import BaseHttpClient as MyHttp

from unit3dup.external.movie_db.trailers.api import YtTrailer
from unit3dup.external.movie_db.tvdb import TVDB

from unit3dup.shared.utility import ManageTitles
from unit3dup.external.media import Media

from unit3dup.view import custom_console
from unit3dup.config.settings import Load

config_settings = Load().config

base_url = "https://api.themoviedb.org/3"

T = TypeVar("T")


# ============================================================================
# TMDB MOVIE ENDPOINTS
# ============================================================================

class MovieEndpoint:

    @staticmethod
    def search(
            query: str,
    ) -> dict:
        return {
            "url": f"{base_url}/search/movie",
            "datatype": Movie,
            "query": query,
            "results": "results",
        }

    @staticmethod
    def playing() -> dict:
        return {
            "url": f"{base_url}/movie/now_playing",
            "datatype": NowPlaying,
            "query": "",
            "results": "results",
        }

    @staticmethod
    def alternative(
            movie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/movie/"
                f"{movie_id}/alternative_titles"
            ),
            "datatype": Alternative,
            "query": "",
            "results": "titles",
        }

    @staticmethod
    def translations(
            movie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/movie/"
                f"{movie_id}/translations"
            ),
            "datatype": MovieTranslation,
            "query": "",
            "results": "translations",
        }

    @staticmethod
    def videos(
            movie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/movie/"
                f"{movie_id}/videos"
            ),
            "datatype": Videos,
            "query": "",
            "results": "results",
        }

    @staticmethod
    def details(
            movie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/movie/"
                f"{movie_id}"
            ),
            "datatype": MovieDetails,
            "query": "",
        }

    @staticmethod
    def keywords(
            movie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/movie/"
                f"{movie_id}/keywords"
            ),
            "datatype": Keyword,
            "query": "",
            "results": "keywords",
        }


# ============================================================================
# TMDB TV ENDPOINTS
# ============================================================================

class TvEndpoint:

    @staticmethod
    def search(
            query: str,
    ) -> dict:
        return {
            "url": f"{base_url}/search/tv",
            "datatype": TvShow,
            "query": query,
            "results": "results",
        }

    @staticmethod
    def playing() -> dict:
        return {
            "url": f"{base_url}/tv/on_the_air",
            "datatype": OnTheAir,
            "query": "",
            "results": "results",
        }

    @staticmethod
    def alternative(
            serie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/tv/"
                f"{serie_id}/alternative_titles"
            ),
            "datatype": Alternative,
            "query": "",
            "results": "results",
        }

    @staticmethod
    def translations(
            serie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/tv/"
                f"{serie_id}/translations"
            ),
            "datatype": TvTranslation,
            "query": "",
            "results": "translations",
        }

    @staticmethod
    def videos(
            serie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/tv/"
                f"{serie_id}/videos"
            ),
            "datatype": Videos,
            "query": "",
            "results": "results",
        }

    @staticmethod
    def details(
            serie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/tv/"
                f"{serie_id}"
            ),
            "datatype": TVShowDetails,
            "query": "",
        }

    @staticmethod
    def keywords(
            serie_id: int,
    ) -> dict:
        return {
            "url": (
                f"{base_url}/tv/"
                f"{serie_id}/keywords"
            ),
            "datatype": Keyword,
            "query": "",
            "results": "keywords",
        }


# ============================================================================
# TMDB API
# ============================================================================

class TmdbAPI:
    """
    TMDB API client.

    Uses MyHttp through composition and dependency injection.

    TmdbAPI is responsible for:
    - TMDB endpoint selection
    - TMDB parameters
    - Response mapping

    MyHttp is responsible for:
    - HTTP communication
    - requests.Session
    - headers
    - cache
    - HTTP requests
    """

    def __init__(
            self,
            client: MyHttp | None = None,
    ) -> None:

        """
        Initialize TMDB API

        Args:
            client:
                Optional MyHttp instance

                If no client is provided, a default MyHttp
                instance is created automatically
        """

        if client is None:
            headers = Agent.headers()

            client = MyHttp(
                headers=headers,
            )

        # Dependency Injection
        self.http_client = client

        # --------------------------------------------------------------
        # Language
        # --------------------------------------------------------------

        if (
                config_settings
                        .user_preferences
                        .PREFERRED_LANG
                        .lower()
                == "all"
        ):
            selected_language = "en-EN"

        else:
            selected_language = (
                config_settings
                .user_preferences
                .PREFERRED_LANG
            )

        # --------------------------------------------------------------
        # Base TMDB parameters
        # --------------------------------------------------------------

        self.params = {
            "api_key": (
                config_settings
                .tracker_config
                .TMDB_APIKEY
            ),
            "language": (
                f"{selected_language.lower()}-"
                f"{selected_language.upper()}"
            ),
        }

        # --------------------------------------------------------------
        # Endpoint mapping
        # --------------------------------------------------------------

        self.ENDPOINTS = {
            "movie": MovieEndpoint,
            "tv": TvEndpoint,
        }

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def _search(
            self,
            query: str,
            category: str,
    ) -> list[T] | None:

        if category not in [
            "movie",
            "tv",
        ]:
            custom_console.bot_warning_log(
                "Check the category of the search query"
            )

            return []

        endpoint_class = self.ENDPOINTS.get(
            category
        )

        if not endpoint_class:
            custom_console.bot_error_log(
                f"Endpoint for category "
                f"'{category}' not found."
            )

            return []

        request = endpoint_class.search(
            query
        )

        return self.request(
            endpoint=request
        )

    # ------------------------------------------------------------------
    # Now playing
    # ------------------------------------------------------------------

    def nowplaying(
            self,
            category: str,
    ) -> list[T] | None:

        endpoint_class = self.ENDPOINTS.get(
            category
        )

        if not endpoint_class:
            custom_console.bot_error_log(
                f"Endpoint for category "
                f"'{category}' not found."
            )

            return []

        request = endpoint_class.playing()

        return self.request(
            endpoint=request
        )

    # ------------------------------------------------------------------
    # Alternative titles
    # ------------------------------------------------------------------

    def alternative(
            self,
            media_id: int,
            category: str,
    ) -> list[T] | None:

        endpoint_class = self.ENDPOINTS.get(
            category
        )

        if not endpoint_class:
            custom_console.bot_error_log(
                f"Endpoint for category "
                f"'{category}' not found."
            )

            return []

        request = endpoint_class.alternative(
            media_id
        )

        return self.request(
            endpoint=request
        )

    # ------------------------------------------------------------------
    # Translations
    # ------------------------------------------------------------------

    def translations(
            self,
            media_id: int,
            category: str,
    ) -> list[T] | None:

        endpoint_class = self.ENDPOINTS.get(
            category
        )

        if not endpoint_class:
            custom_console.bot_error_log(
                f"Endpoint for category "
                f"'{category}' not found."
            )

            return []

        request = endpoint_class.translations(
            media_id
        )

        return self.request(
            endpoint=request
        )

    # ------------------------------------------------------------------
    # Videos
    # ------------------------------------------------------------------

    def _videos(
            self,
            video_id: int,
            category: str,
    ) -> list[T] | None:

        endpoint_class = self.ENDPOINTS.get(
            category
        )

        if not endpoint_class:
            custom_console.bot_error_log(
                f"Endpoint for category "
                f"'{category}' not found."
            )

            return []

        request = endpoint_class.videos(
            video_id
        )

        return self.request(
            endpoint=request
        )

    # ------------------------------------------------------------------
    # Details
    # ------------------------------------------------------------------

    def details(
            self,
            video_id: int,
            category: str,
    ) -> list[T] | None:

        endpoint_class = self.ENDPOINTS.get(
            category
        )

        if not endpoint_class:
            custom_console.bot_error_log(
                f"Endpoint for category "
                f"'{category}' not found."
            )

            return []

        request = endpoint_class.details(
            video_id
        )

        return self.request(
            endpoint=request
        )

    # ------------------------------------------------------------------
    # Keywords
    # ------------------------------------------------------------------

    def _keywords(
            self,
            video_id: int,
            category: str,
    ) -> list[T] | None:

        endpoint_class = self.ENDPOINTS.get(
            category
        )

        if not endpoint_class:
            custom_console.bot_error_log(
                f"Endpoint for category "
                f"'{category}' not found."
            )

            return []

        request = endpoint_class.keywords(
            video_id
        )

        return self.request(
            endpoint=request
        )

    # ------------------------------------------------------------------
    # HTTP request
    # ------------------------------------------------------------------

    def request(
            self,
            endpoint: dict,
    ) -> list[T] | None:

        """
        Execute a TMDB API request through MyHttp.

        MyHttp handles:
        - HTTP communication
        - requests.Session
        - headers
        - cache

        TmdbAPI handles:
        - TMDB endpoint selection
        - TMDB parameters
        - response mapping
        """

        params = {
            **self.params,
            "query": endpoint.get(
                "query",
                "",
            ),
        }

        response = self.http_client.get_url(
            url=endpoint["url"],
            params=params,
            use_cache=True,
        )

        if response is None:
            return None

        if response.status_code != 200:
            return []

        try:

            response_data = response.json()

        except ValueError:

            custom_console.bot_error_log(
                "TMDB returned an invalid JSON response."
            )

            return []

        results_key = endpoint.get(
            "results"
        )

        if results_key:

            response_data = response_data.get(
                results_key,
                [],
            )

        else:

            response_data = [
                response_data
            ]

        return [
            endpoint["datatype"](
                **attribute
            )
            for attribute in response_data
        ]


# ============================================================================
# DB ONLINE
# ============================================================================

class DbOnline(TmdbAPI):

    def __init__(
            self,
            media: Media,
            no_title=None,
            client: MyHttp | None = None,
    ) -> None:

        """
        Initialize DbOnline.

        The MyHttp instance can be injected from outside.

        Example:

            http_client = MyHttp(
                headers=Agent.headers()
            )

            db_online = DbOnline(
                media=media,
                client=http_client
            )
        """

        super().__init__(
            client=client,
        )

        self.media = media
        self.category = media.category
        self.query = media.guess_title

        self.imdb_id = None
        self.tvdb_id = None

        # --------------------------------------------------------------
        # Local application cache
        # --------------------------------------------------------------

        if (
                config_settings
                        .user_preferences
                        .CACHE_DBONLINE
        ):
            self.cache = diskcache.Cache(
                str(
                    os.path.join(
                        config_settings
                        .user_preferences
                        .CACHE_PATH,
                        "tmdb.cache",
                    )
                )
            )

        # --------------------------------------------------------------
        # Search by IDs
        # --------------------------------------------------------------

        if (
                media.tmdb_id
                or media.imdb_id
                or media.tvdb_id
        ):

            self.media_result = (
                self.results_in_string(
                    tmdb_id=int(
                        media.tmdb_id
                    ),
                    imdb_id=int(
                        media.imdb_id
                    ),
                    tvdb_id=int(
                        media.tvdb_id
                    ),
                )
            )

        else:

            if no_title:
                self.query = no_title

            self.media_result = self.search()

    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------

    @staticmethod
    def hash_key(
            key: str,
    ) -> str:

        return hashlib.md5(
            key.encode(
                "utf-8"
            )
        ).hexdigest()

    # ------------------------------------------------------------------
    # Match result
    # ------------------------------------------------------------------

    def is_like(
            self,
            results: list[T],
    ) -> T | bool:

        if results:

            # ----------------------------------------------------------
            # Search by title and original title
            # ----------------------------------------------------------

            for result in results:

                if (
                        result.get_date()
                        and
                        self.media
                                .guess_filename
                                .guessit_year
                ):

                    if not (
                            datetime.strptime(
                                result.get_date(),
                                "%Y-%m-%d",
                            ).year
                            ==
                            self.media
                                    .guess_filename
                                    .guessit_year
                    ):
                        continue

                if (
                        ManageTitles.fuzzyit(
                            str1=(
                                    ManageTitles
                                            .clean_text(
                                        self.query
                                    )
                            ),
                            str2=(
                                    ManageTitles
                                            .clean_text(
                                        result
                                                .get_title()
                                    )
                            ),
                        )
                        > 95
                ):
                    return result

                if (
                        ManageTitles.fuzzyit(
                            str1=(
                                    ManageTitles
                                            .clean_text(
                                        self.query
                                    )
                            ),
                            str2=(
                                    ManageTitles
                                            .clean_text(
                                        result
                                                .get_original()
                                    )
                            ),
                        )
                        > 95
                ):
                    return result

            # ----------------------------------------------------------
            # Search alternative titles
            # ----------------------------------------------------------

            for result in results:

                alternative = self.alternative(
                    media_id=result.id,
                    category=self.category,
                )

                if alternative:

                    for alt in alternative:

                        if (
                                ManageTitles.fuzzyit(
                                    str1=self.query,
                                    str2=alt.title,
                                )
                                > 95
                        ):
                            return result

            # ----------------------------------------------------------
            # Search translations
            # ----------------------------------------------------------

            for result in results:

                translations = self.translations(
                    media_id=result.id,
                    category=self.category,
                )

                if translations:

                    for tr in translations:

                        if tr.data:

                            title = (
                                    tr.data.name
                                    or tr.data.title
                            )

                            if title:

                                if (
                                        ManageTitles.fuzzyit(
                                            self.query,
                                            title,
                                        )
                                        > 95
                                ):
                                    return result

        return False

    # ------------------------------------------------------------------
    # Results from ID
    # ------------------------------------------------------------------

    def results_in_string(
            self,
            tmdb_id: int,
            imdb_id: int,
            tvdb_id: int,
    ) -> MediaResult:

        keywords_list = ""
        trailer_key = ""

        if tmdb_id:

            if tmdb_id > 0:
                trailer_key = self.trailer(
                    tmdb_id
                )

                keywords_list = (
                    self.keywords(
                        tmdb_id
                    )
                    if trailer_key
                    else ""
                )

        else:

            tmdb_id = 0

        search_results = MediaResult(
            video_id=tmdb_id,
            imdb_id=self.imdb_id,
            tvdb_id=tvdb_id,
            trailer_key=trailer_key,
            keywords_list=keywords_list,
        )

        self.print_results(
            results=search_results
        )

        return search_results

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
            self,
    ) -> MediaResult | None:

        # --------------------------------------------------------------
        # Local cache
        # --------------------------------------------------------------

        if (
                config_settings
                        .user_preferences
                        .CACHE_DBONLINE
        ):

            search_results = self.load_cache(
                self.hash_key(
                    self.query
                )
            )

            if search_results:
                self.print_results(
                    results=search_results
                )

                return search_results

        # --------------------------------------------------------------
        # TMDB search
        # --------------------------------------------------------------

        results = self._search(
            self.query,
            self.category,
        )

        # --------------------------------------------------------------
        # TVDB search
        # --------------------------------------------------------------

        tvdb_result = self.tvdb_search()

        if tvdb_result:
            self.tvdb_id = tvdb_result.get(
                "tvdb_id",
                None,
            )

            self.imdb_id = tvdb_result.get(
                "imdb_id",
                None,
            )

        # --------------------------------------------------------------
        # Match result
        # --------------------------------------------------------------

        if results:

            if result := self.is_like(
                    results
            ):

                trailer_key = self.trailer(
                    result.id
                )

                keywords_list = self.keywords(
                    result.id
                )

                search_results = MediaResult(
                    result,
                    video_id=result.id,
                    imdb_id=self.imdb_id,
                    tvdb_id=self.tvdb_id,
                    trailer_key=trailer_key,
                    keywords_list=keywords_list,
                )

                self.print_results(
                    results=search_results
                )

                # ------------------------------------------------------
                # Save local cache
                # ------------------------------------------------------

                if (
                        config_settings
                                .user_preferences
                                .CACHE_DBONLINE
                ):
                    self.cache[
                        self.hash_key(
                            self.query
                        )
                    ] = search_results

                return search_results

        # --------------------------------------------------------------
        # TMDB unavailable
        # --------------------------------------------------------------

        if results is None:
            custom_console.bot_error_log(
                "TMDB - No response from the remote host "
                "or the API key is invalid. "
                "Retry or update your key"
            )

            exit(1)

        # --------------------------------------------------------------
        # No result found
        # --------------------------------------------------------------

        custom_console.bot_warning_log(
            "Title not found. "
            "What the bot has understood:"
        )

        custom_console.bot_warning_log(
            f"Title: '{self.query}'\n"
            f"category: '{self.category}'"
        )

        if self.category in "tv":

            serie = (
                f"S{str(self.media.guess_season).zfill(2)}"
                if self.media.guess_season
                else ""
            )

            if not self.media.torrent_pack:
                serie += (
                    f"E{str(self.media.guess_episode).zfill(2)}"
                )

            custom_console.bot_warning_log(
                f"details: '{serie}' "
                f"Pack: '{self.media.torrent_pack}'"
            )

        # --------------------------------------------------------------
        # Manual search
        # --------------------------------------------------------------

        search_results = self.manual_search()

        if (
                config_settings
                        .user_preferences
                        .CACHE_DBONLINE
        ):
            self.cache[
                self.hash_key(
                    self.query
                )
            ] = search_results

        return search_results

    # ------------------------------------------------------------------
    # TVDB
    # ------------------------------------------------------------------

    def tvdb_search(
            self,
    ) -> dict | None:

        tvdb = TVDB(
            category=self.category
        )

        return tvdb.search(
            query=self.query
        )

    # ------------------------------------------------------------------
    # Manual TMDB search
    # ------------------------------------------------------------------

    def manual_search(
            self,
    ) -> MediaResult | None:

        user_id = 0

        while True:

            if not (
                    config_settings
                            .user_preferences
                            .SKIP_TMDB
            ):

                try:

                    user_id = (
                        custom_console
                        .user_input(
                            message=(
                                "Please digit a valid "
                                "TMDB ID (0=skip)->"
                            )
                        )
                    )

                except KeyboardInterrupt:

                    custom_console.bot_error_log(
                        "\nOperation cancelled"
                    )

                    exit(0)

            else:

                custom_console.bot_warning_log(
                    "\n ** Auto skip TMDB ID **\n"
                )

            # ----------------------------------------------------------
            # Skip TMDB
            # ----------------------------------------------------------

            if user_id == 0:
                trailer_key = (
                    self.youtube_trailer()
                )

                search_results = MediaResult(
                    video_id=user_id,
                    imdb_id=self.imdb_id,
                    trailer_key=trailer_key,
                    keywords_list="not available",
                )

                self.print_results(
                    results=search_results
                )

                return search_results

            # ----------------------------------------------------------
            # Search TMDB ID
            # ----------------------------------------------------------

            result = self.search_id(
                video_id=user_id
            )

            if result:
                trailer_key = self.trailer(
                    user_id
                )

                keywords_list = (
                    self.keywords(
                        user_id
                    )
                    if trailer_key
                    else ""
                )

                search_results = MediaResult(
                    result=result,
                    video_id=user_id,
                    imdb_id=self.imdb_id,
                    trailer_key=trailer_key,
                    keywords_list=keywords_list,
                )

                self.print_results(
                    results=search_results
                )

                return search_results

    # ------------------------------------------------------------------
    # YouTube trailer
    # ------------------------------------------------------------------

    def youtube_trailer(
            self,
    ) -> str | None:

        if (
                "no_key"
                in config_settings
                .tracker_config
                .YOUTUBE_KEY
        ):
            return "not available"

        if (
                config_settings
                        .user_preferences
                        .SKIP_YOUTUBE
        ):
            return "Skipped"

        yt_trailer = YtTrailer(
            self.query
        )

        result = (
            yt_trailer
            .get_trailer_link()
        )

        if result:

            for r in result:

                title = (
                    r.items[0]
                    .snippet
                    .title
                    if r.items
                    else None
                )

                if (
                        title
                        and self.query in title
                ):
                    return (
                        r.items[0]
                        .id
                        .videoId
                    )

            return "not available"

        user_youtube_id = (
            custom_console
            .user_input_str(
                message=(
                    "Sorry trailer not found. "
                    "Please digit a valid "
                    "Youtube ID (0=skip)->"
                )
            )
        )

        if user_youtube_id == 0:
            return "not available"

        return user_youtube_id

    # ------------------------------------------------------------------
    # TMDB trailer
    # ------------------------------------------------------------------

    def trailer(
            self,
            video_id: int,
    ) -> str | None:

        trailers = self._videos(
            video_id,
            self.category,
        )

        if trailers:

            trailer = next(
                (
                    video
                    for video in trailers
                    if video.site.lower()
                       == "youtube"
                ),
                None,
            )

            if trailer:
                return trailer.key

            return "not available"

        return self.youtube_trailer()

    # ------------------------------------------------------------------
    # Keywords
    # ------------------------------------------------------------------

    def keywords(
            self,
            video_id: int,
    ) -> str | None:

        keywords_list = (
            self._keywords(
                video_id,
                self.category,
            )
        )

        if keywords_list:
            return ",".join(
                [
                    key.name
                    for key in keywords_list
                ]
            )

        return "not available"

    # ------------------------------------------------------------------
    # Print results
    # ------------------------------------------------------------------

    def print_results(
            self,
            results: MediaResult,
    ) -> None:

        custom_console.bot_log(
            f"'TMDB TITLE'..... "
            f"{self.query}"
        )

        custom_console.bot_log(
            f"'TMDB ID'........ "
            f"{results.video_id}"
        )

        if results.imdb_id:
            custom_console.bot_warning_log(
                f"'IMDB ID'........ "
                f"'{results.imdb_id}'"
            )

        if results.tvdb_id:
            custom_console.bot_warning_log(
                f"'TVDB ID'........ "
                f"'{results.tvdb_id}'"
            )

        custom_console.bot_log(
            f"'TMDB KEYWORDS'.. "
            f"{results.keywords_list}"
        )

        if results.trailer_key.upper() in [
            "SKIPPED",
            "NOT AVAILABLE",
        ]:

            custom_console.bot_log(
                f"'TRAILER' ....... "
                f"{results.trailer_key}"
            )

        else:

            custom_console.bot_log(
                "'TRAILER' ....... "
                "https://www.youtube.com/watch?v="
                f"{results.trailer_key}"
            )

    # ------------------------------------------------------------------
    # Load local cache
    # ------------------------------------------------------------------

    def load_cache(
            self,
            query: str,
    ) -> MediaResult | None:

        if query not in self.cache:
            return None

        custom_console.bot_warning_log(
            "<> Using cached results"
        )

        try:

            return self.cache[
                query
            ]

        except KeyError:

            custom_console.bot_error_log(
                "Cached frame not found or "
                "cache file corrupted"
            )

            custom_console.bot_error_log(
                "Proceed to extract the screenshot "
                "again. Please wait.."
            )

            return None

    # ------------------------------------------------------------------
    # Search by TMDB ID
    # ------------------------------------------------------------------

    def search_id(
            self,
            video_id: int,
    ) -> list[T] | None:

        result = self.details(
            video_id=video_id,
            category=self.category,
        )

        if result:
            return result[0]

        return None
