# -*- coding: utf-8 -*-

import requests
from ..config import config


class LatestRelease:
    """
    Class for handling information about the latest movie releases via the TMDB API

    Attributes:
        base_url (str): The base URL for the TMDB API
        language (str): The language to use for the API requests
        params (dict): The parameters for the API requests
    """

    base_url = "https://api.themoviedb.org/3"
    language = "it-IT"
    params = {"api_key": config.TMDB_APIKEY}

    def __init__(self, releases: dict):
        """
        Initializes an instance of the LatestRelease class

        Args:
            releases (dict): The release data retrieved from the API
        """
        self.releases = releases

    @classmethod
    def get_latest(cls, movie_id: str):
        """
        Retrieves the latest release information for a specified movie

        Args:
            movie_id (str): The ID of the movie to retrieve information for

        Returns:
            LatestRelease: An instance of the LatestRelease class with the release data
        """
        endpoint = f"{cls.base_url}/movie/{movie_id}/release_dates"
        response = requests.get(endpoint, params=cls.params)

        if response.status_code == 200:
            releases = response.json().get("results", [])
            return cls(releases)
        return None

    def release_date(self):
        """
        Retrieves the release date for Italy, if available

        Returns:
            str: The release date in Italy if available, otherwise None
        """
        for release in self.releases:
            if release["iso_3166_1"] == "IT":  # TODO: add languages
                for date_info in release["release_dates"]:
                    release_date = date_info.get("release_date")
                    if release_date:
                        return release
        return None


class NowPlaying:
    """
    Class for handling information about currently playing movies via the TMDB API

    Attributes:
        base_url (str): The base URL for the TMDB API
        language (str): The language to use for the API requests
        params (dict): The parameters for the API requests
    """

    base_url = "https://api.themoviedb.org/3"
    language = "it-IT"
    params = {"api_key": config.TMDB_APIKEY, "language": language, "page": 1}

    def __init__(self, movie_id=None, title=None, release_date=None):
        """
        Initializes an instance of the NowPlaying class

        Args:
            releases (dict): The data about currently playing movies
            movie_id (Optional[int]): The ID of the movie
            title (Optional[str]): The title of the movie
            release_date (Optional[str]): The release date of the movie
        """
        # self.releases = releases
        self.movie_id = movie_id
        self.title = title
        self.release_date = release_date

    @classmethod
    def create_instance(cls, movie_id, title, release_date):
        """
        Creates a new instance of the NowPlaying class

        Args:
            releases (dict): The data about currently playing movies
            movie_id (int): The ID of the movie
            title (str): The title of the movie
            release_date (str): The release date of the movie

        Returns:
            NowPlaying: A new instance of the NowPlaying class
        """
        return cls(movie_id, title, release_date)

    @classmethod
    def get_now_playing(cls) -> list['NowPlaying']:
        """
        Retrieves the currently playing movies

        Returns:
            list[NowPlaying]: A list of NowPlaying instances for the currently playing movies
        """
        endpoint = f"{cls.base_url}/movie/now_playing"
        response = requests.get(endpoint, params=cls.params)

        if response.status_code == 200:
            movies = response.json().get("results", [])
            new_instances = []

            for movie in movies:
                instance = cls.create_instance(
                    movie_id=movie["id"],
                    title=movie["title"],
                    release_date=movie.get("release_date", "Unknown"),
                )

                new_instances.append(instance)
                """
                print(
                    f"Title: {instance.title}, ID: {instance.movie_id}, Release Date: {instance.release_date}"
                )
                """

            return new_instances

        else:
            print(f"Request error: {response.status_code}")
            return []


class LatestReleaseAirTvShow:
    """
    Class for handling information about TV shows currently airing via the TMDB API

    Attributes:
        base_url (str): The base URL for the TMDB API
        language (str): The language to use for the API requests
        params (dict): The parameters for the API requests
    """

    base_url = "https://api.themoviedb.org/3"
    language = "it-IT"
    params = {
        "api_key": config.TMDB_APIKEY,
        "language": language,
        "page": 1,
    }

    def __init__(self, tv_shows: dict):
        """
        Initializes an instance of the LatestReleaseAirTvShow class

        Args:
            tv_shows (dict): The data about currently airing TV shows
        """
        self.tv_shows = tv_shows

    @classmethod
    def get_latest(cls, movie_id: str):
        """
        Retrieves information about currently airing TV shows

        Args:
            movie_id (str): The ID of the movie (although not used in this request)

        Returns:
            LatestReleaseAirTvShow: An instance of the LatestReleaseAirTvShow class with the TV show data
        """
        endpoint = f"{cls.base_url}/tv/on_the_air"
        response = requests.get(endpoint, params=cls.params)
        if response.status_code == 200:
            tv_shows = response.json().get("results", [])
            return cls(tv_shows)
        return None

    def release_date(self):
        """
        information about TV shows, including the first air date

        Returns:
            None
        """
        for show in self.tv_shows:
            print(f"Title: {show['name']}, First Air Date: {show['first_air_date']}")
