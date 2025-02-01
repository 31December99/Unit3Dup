# -*- coding: utf-8 -*-
import json

from common.external_services.theMovieDB.core import config
from common.external_services.sessions.session import MyHttp
from common.external_services.sessions.agents import Agent
from common.external_services.theMovieDB.core.models.multi import Movie,TVShow

base_url = "https://api.themoviedb.org/3"
ENABLE_LOG = True


class TmdbMultiApi(MyHttp):
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

    def multi(self, query: str, category: int) -> list:
        """
        Retrieves results from the multi-search API of TMDb based on the query.
        """
        params = {**TmdbMultiApi.params, "query": query}
        media =  []
        response = self.get_url(f"{base_url}/search/multi", params=params).json()


        for result in response['results']:
            media_type = result['media_type'].lower().strip()
            if category==1:
                if media_type == "movie":
                    media.append(Movie(**result))

            if category==2:
                if media_type == "tv":
                    media.append(TVShow(**result))
        return media


    def videos(self, query: str, video_id: int, category: str)-> json:
        params = {**TmdbMultiApi.params, "query": query}
        return self.get_url(f"{base_url}/{category}/{video_id}/videos", params=params).json()


    def keywords(self, query: str, video_id: int, category: str)-> json:
        params = {**TmdbMultiApi.params, "query": query}
        return self.get_url(f"{base_url}/{category}/{video_id}/keywords", params=params).json()

