# -*- coding: utf-8 -*-
import pprint
from common.config import config
from common.external_services.sessions.session import MyHttp
from common.external_services.sessions.agents import Agent
from common.external_services.theMovieDB.core.models.tvshow_on_the_air import OnTheAir
from common.external_services.theMovieDB.core.models.tvshow import TvShow
from common.external_services.theMovieDB.core.exceptions import exception_handler
from common.external_services.theMovieDB.core.models.translations import (
    Translation,
    TranslationsResponse,
)


from common.external_services.theMovieDB.core.models.tvshow_details import (
    TVShow,
    LastEpisodeToAir,
    Genre,
    SpokenLanguage,
    CreatedBy,
    Network,
    ProductionCompany,
    ProductionCountry,
    Season,
)


base_url = "https://api.themoviedb.org/3"


class TmdbTvShowApi(MyHttp):
    params = {
        "api_key": config.TMDB_APIKEY,
        "language": "it-IT",
    }

    def __init__(self):
        """
        Initialize the TvShowApi instance with an HTTP client
        """
        headers = Agent.headers()
        super().__init__(headers)
        self.http_client = self.session

    @exception_handler
    def on_the_air(self) -> list[OnTheAir]:
        """
        Retrieves the list of TV shows that are currently on the air
        """
        response = self.get_url(
            f"{base_url}/tv/on_the_air", params=TmdbTvShowApi.params
        )
        if response.status_code == 200:
            tv_latest = response.json().get("results", [])
            return [OnTheAir(**tv_data) for tv_data in tv_latest]
        else:
            print(f"Request error: {response.status_code}")
            return []

    @exception_handler
    def tv_show_translations(self, tv_show_id: int) -> TranslationsResponse:
        """
        Retrieves the translations for a specified TV show and returns them as a TranslationsResponse object
        """
        response = self.get_url(
            f"{base_url}/tv/{tv_show_id}/translations", params=TmdbTvShowApi.params
        )
        data = response.json()
        translations = [
            Translation(
                iso_639_1=item.get("iso_639_1", ""),
                english_name=item.get("english_name", ""),
                name=item.get("name", ""),
                url=item.get("url", ""),  # url is optional
                tagline=item.get("tagline", ""),
                description=item.get("description", ""),
                country=item.get("country", ""),
            )
            for item in data.get("translations", [])
        ]
        return TranslationsResponse(translations=translations)

    @exception_handler
    def tv_show_details(self, tv_show_id: int):
        """
        Retrieves the details for a specified TV show
        """
        response = self.get_url(
            f"{base_url}/tv/{tv_show_id}", params=TmdbTvShowApi.params
        )
        if response.status_code == 200:
            tv_show_data = response.json()


            # Convert nested dictionaries/lists to respective dataclass instances
            # Pass the dictionary keys as arguments to the function ( **)

            tv_show_data["last_episode_to_air"] = LastEpisodeToAir(
                **tv_show_data.get("last_episode_to_air", {})
            )
            tv_show_data["next_episode_to_air"] = (
                LastEpisodeToAir(**tv_show_data.get("next_episode_to_air", {}))
                if tv_show_data.get("next_episode_to_air")
                else None
            )

            tv_show_data["genres"] = [
                Genre(**genre) for genre in tv_show_data.get("genres", [])
            ]
            tv_show_data["created_by"] = [
                CreatedBy(**creator) for creator in tv_show_data.get("created_by", [])
            ]
            tv_show_data["networks"] = [
                Network(**network) for network in tv_show_data.get("networks", [])
            ]
            tv_show_data["production_companies"] = [
                ProductionCompany(**company)
                for company in tv_show_data.get("production_companies", [])
            ]
            tv_show_data["production_countries"] = [
                ProductionCountry(**country)
                for country in tv_show_data.get("production_countries", [])
            ]
            tv_show_data["seasons"] = [
                Season(**season) for season in tv_show_data.get("seasons", [])
            ]
            tv_show_data["spoken_languages"] = [
                SpokenLanguage(**language)
                for language in tv_show_data.get("spoken_languages", [])
            ]

            tv_show = TVShow(**tv_show_data)

            return tv_show
        else:
            print(f"Request error: {response.status_code}")
            return {}

    @exception_handler
    def tv_watch_providers(self, tv_show_id: int):
        """
        Retrieves the watch providers for a specified TV show
        """
        response = self.get_url(
            f"{base_url}/tv/{tv_show_id}/watch/providers", params=TmdbTvShowApi.params
        )
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Request error: {response.status_code}")
            return []

    @exception_handler
    def tv_show_airing_today(self):
        """
        Retrieves a list of TV shows that are airing today
        """
        response = self.get_url(
            f"{base_url}/tv/airing_today", params=TmdbTvShowApi.params
        )
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Request error: {response.status_code}")
            return []

    @exception_handler
    def tv_show_popular(self):
        """
        Retrieves a list of popular TV shows
        """
        response = self.get_url(f"{base_url}/tv/popular", params=TmdbTvShowApi.params)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Request error: {response.status_code}")
            return []

    @exception_handler
    def tv_show_top_rated(self):
        """
        Retrieves a list of top-rated TV shows
        """
        response = self.get_url(f"{base_url}/tv/top_rated", params=TmdbTvShowApi.params)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Request error: {response.status_code}")
            return []

    @exception_handler
    def search_tv_shows(self, query: str) -> list["TvShow"]:
        """
        Searches for TV shows based on a query
        """
        params = {**TmdbTvShowApi.params, "query": query}
        response = self.get_url(f"{base_url}/search/tv", params=params, use_cache=False)
        if response.status_code == 200:
            tv_show_results = response.json().get("results", [])
            return [TvShow(**tv_data) for tv_data in tv_show_results]
        else:
            print(f"Request error: {response.status_code}")
            return []

    @exception_handler
    def tv_genres(self):
        """
        Retrieves the list of TV show genres
        """
        response = self.get_url(
            f"{base_url}/genre/tv/list", params=TmdbTvShowApi.params
        )
        if response.status_code == 200:
            return response.json().get("genres", [])
        else:
            print(f"Request error: {response.status_code}")
            return {}
