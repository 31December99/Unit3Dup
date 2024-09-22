# -*- coding: utf-8 -*-

from common.config import config
from common.external_services.sessions.agents import Agent
from common.external_services.sessions.session import MyHttp
from common.external_services.Pw.core.models.indexers import Indexer
from common.external_services.Pw.core.models.search import Search
from common.external_services.Pw.core.models.torrent_client_config import (
    TorrentClientConfig,
)


class PwAPI(MyHttp):

    def __init__(self):
        """
        Initialize the PwApi instance
        """
        headers = Agent.headers()
        headers.update(
            {"X-Api-Key": config.PW_API_KEY, "Content-Type": "application/json"}
        )

        super().__init__(headers)
        self.http_client = self.session
        self.base_url = config.PW_URL
        self.api_key = config.PW_API_KEY
        self.dataclass = {f"{self.base_url}/indexer": Indexer}

    def get_indexers(self) -> ["Indexer"]:
        """Get all indexers."""

        response = self.get_url(url=f"{self.base_url}/indexer", params={})

        if response.status_code == 200:
            indexers_list = response.json()
            return [Indexer(**indexer) for indexer in indexers_list]
        else:
            return []

    def search(self, query: str) -> ["Search"]:
        """Get search queue."""

        params = {"query": query}
        url = f"{self.base_url}/search?"

        response = self.get_url(url=url, params=params)

        if response.status_code == 200:
            results_list = response.json()
            return [Search(**result) for result in results_list]
        else:
            return []

    def get_torrent_client_ids(self) -> list["TorrentClientConfig"]:
        """Get a list of torrent client configurations"""

        url = f"{self.base_url}/downloadclient"
        response = self.get_url(url=url, params={})

        if response.status_code == 200:
            configurations_list = response.json()
            return [
                TorrentClientConfig(**client_config)
                for client_config in configurations_list
            ]
        else:
            return []

    def send_torrent_to_client(self, payload):
        """send torrent to client"""

        url = f"{self.base_url}/downloadclient/1"
        response = self.get_url(url=url, body=payload, get_method=False)

        # TODO: Test again - get_url() updated 21/09/2024
        if response.status_code == 202 or response.status_code == 200:
            result = response.json()
        else:
            return []
