# -*- coding: utf-8 -*-
import pprint

from common.config import config
from common.external_services.sessions.session import MyHttp
from common.external_services.sessions.agents import Agent
from common.external_services.theMovieDB.core.models.movie.nowplaying import NowPlaying
from common.external_services.theMovieDB.core.models.movie.release_info import (
    MovieReleaseInfo,
)
from common.external_services.theMovieDB.core.models.movie.alternative_titles import (
    AltTitle,
    Title,
)

base_url = "https://api.themoviedb.org/3"
ENABLE_LOG = True


class TmdbMovieApi(MyHttp):
    params = {
        "api_key": config.TMDB_APIKEY,
        "language": "it-IT",
    }

    def __init__(self):
        """
        Initialize the MovieApi instance with an HTTP client
        """
        headers = Agent.headers()
        super().__init__(headers)
        self.http_client = self.session

    def now_playing(self) -> list[NowPlaying]:
        """
        Retrieves the currently playing movies
        """
        response = self.get_url(
            f"{base_url}/movie/now_playing", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            movies_list = response.json().get("results", [])
            return [NowPlaying(**movie_data) for movie_data in movies_list]
        else:
            print(f"Request error: {response.status_code}")
            return []

    def latest_movie(self, now_playing: NowPlaying) -> list[MovieReleaseInfo]:
        """
        Retrieves the latest release information for a specified movie
        """
        response = self.get_url(
            f"{base_url}/movie/{now_playing.id}/release_dates",
            params=TmdbMovieApi.params,
        )

        if response.status_code == 200:
            movie_latest = response.json().get("results", [])
            pprint.pprint(movie_latest)

            # Use the class method to create and validate MovieReleaseInfo instances
            release_info_list = [
                MovieReleaseInfo.validate_data(movie_data)
                for movie_data in movie_latest
            ]

            # Filter out None values (invalid data)
            return [info for info in release_info_list if info is not None]
        else:
            print(f"Request error: {response.status_code}")
            return []

    def movie_details(self, movie_id: int):
        """
        Retrieves the details for a specified movie
        """
        response = self.get_url(
            f"{base_url}/movie/{movie_id}", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request error: {response.status_code}")
            return {}

    def movie_credits(self, movie_id: int):
        """
        Retrieves the credits (cast and crew) for a specified movie
        """
        response = self.get_url(
            f"{base_url}/movie/{movie_id}/credits", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request error: {response.status_code}")
            return {}

    def movie_images(self, movie_id: int):
        """
        Retrieves the images for a specified movie
        """
        response = self.get_url(
            f"{base_url}/movie/{movie_id}/images", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request error: {response.status_code}")
            return {}

    def movie_videos(self, movie_id: int):
        """
        Retrieves the videos (trailers, etc.) for a specified movie
        """
        response = self.get_url(
            f"{base_url}/movie/{movie_id}/videos", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request error: {response.status_code}")
            return {}

    def movie_similar(self, movie_id: int):
        """
        Retrieves a list of similar movies to the specified movie
        """
        response = self.get_url(
            f"{base_url}/movie/{movie_id}/similar", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Request error: {response.status_code}")
            return []

    def movie_recommendations(self, movie_id: int):
        """
        Retrieves a list of recommended movies based on the specified movie
        """
        response = self.get_url(
            f"{base_url}/movie/{movie_id}/recommendations", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Request error: {response.status_code}")
            return []

    def movie_alternative_title(self, movie_id: int) -> list["AltTitle"]:
        """
        Retrieves a list of recommended movies based on the specified movie
        """

        response = self.get_url(
            f"{base_url}/movie/{movie_id}/alternative_titles",
            params=TmdbMovieApi.params,
        )

        if response:
            data = response.json()
            titles = data.get("titles", [])

            return [
                # Create AltTitle object with an unique id movie_id
                AltTitle(
                    id=movie_id,
                    # Add the titles
                    titles=[
                        Title.from_dict(title_data)
                        for title_data in titles
                        # Add it only if the json attribute name is identical to the @dataclass attribute
                        if Title.from_dict(title_data) is not None
                    ],
                )
            ]
        else:
            return []

    def search_movies(self, query: str):
        """
        Searches for movies based on a query
        """
        params = {**TmdbMovieApi.params, "query": query}
        response = self.get_url(f"{base_url}/search/movie", params=params)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Request error: {response.status_code}")
            return []

    def movie_genres(self):
        """
        Retrieves the list of movie genres
        """
        response = self.get_url(
            f"{base_url}/genre/movie/list", params=TmdbMovieApi.params
        )
        if response.status_code == 200:
            return response.json().get("genres", [])
        else:
            print(f"Request error: {response.status_code}")
            return {}