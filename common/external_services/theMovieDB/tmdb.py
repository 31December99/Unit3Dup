# -*- coding: utf-8 -*-

from ...config import config
from common.external_services.sessions.session import MyHttp
from common.external_services.theMovieDB.response import (
    NowPlaying,
    MovieReleaseInfo,
    TvShow,
)
from common.external_services.sessions.agents import Agent

base_url = "https://api.themoviedb.org/3"


class Tmdb(MyHttp):
    params = {
        "api_key": config.TMDB_APIKEY,
        "language": "it-IT",
    }

    def __init__(self):
        """
        Initialize the Tmdb instance with an HTTP client.

        Args:
            my_http (MyHttp): An instance of MyHttp class for making HTTP requests.
        """

        headers = Agent.headers()
        super().__init__(headers)
        self.http_client = self.session

    def get_now_playing(self) -> list["NowPlaying"]:
        """
        Retrieves the currently playing movies

        Returns:
            list[Movie]: A list of Movie instances for the currently playing movies
        """

        # Nowplaying Endpoint
        response = self.get_url(
            f"{base_url}/movie/now_playing", params=Tmdb.params
        )

        if response.status_code == 200:
            movies_list = response.json().get("results", [])
            # For each movie creates an Movie() object
            return [NowPlaying(**movie_data) for movie_data in movies_list]
        else:
            print(f"Request error: {response.status_code}")
            return []

    def get_latest_movie(self, now_playing: NowPlaying) -> list["MovieReleaseInfo"]:
        """
        Retrieves the latest release information for a specified movie

        Args:
            now_playing: (NowPlaying) The ID of the movie to retrieve information for

        Returns:
            LatestRelease: An instance of the LatestRelease class with the release data
        """

        response = self.get_url(
            f"{base_url}/movie/{now_playing.id}/release_dates", params=Tmdb.params
        )

        if response.status_code == 200:
            movie_latest = response.json().get("results", [])
            # For each movie creates an Movie() object
            return [MovieReleaseInfo(**movie_data) for movie_data in movie_latest]
        else:
            print(f"Request error: {response.status_code}")
            return []

    def get_tv_show(self):

        response = self.get_url(f"{base_url}/tv/on_the_air", params=Tmdb.params)

        if response.status_code == 200:
            tv_latest = response.json().get("results", [])
            return [TvShow(**tv_data) for tv_data in tv_latest]

        else:
            print(f"Request error: {response.status_code}")
            return []
