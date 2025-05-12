# -*- coding: utf-8 -*-
import os.path

from common.external_services.Pw.core.models.torrent_client_config import (
    TorrentClientConfig,
)
from common.external_services.Pw.core.models.indexers import Indexer
from common.external_services.Pw.core.models.search import Search
from common.external_services.sessions.session import MyHttp
from common.external_services.sessions.agents import Agent
from common import config_settings

from view import custom_console

class PwAPI(MyHttp):

    def __init__(self):
        """
        Initialize the PwApi instance
        """
        headers = Agent.headers()
        headers.update(
            {"X-Api-Key": config_settings.options.PW_API_KEY, "Content-Type": "application/json"}
        )

        super().__init__(headers)
        self.http_client = self.session
        self.base_url = config_settings.options.PW_URL
        self.api_key = config_settings.options.PW_API_KEY
        self.dataclass = {f"{self.base_url}/indexer": Indexer}

        if not config_settings.options.PW_URL:
            custom_console.bot_question_log("No PW_URL provided\n")
            exit(1)

        if not config_settings.options.PW_API_KEY:
            custom_console.bot_question_log("No PW_API_KEY provided\n")
            exit(1)

    def get_indexers(self) -> list[type[[Indexer]]]:
        """Get all indexers."""

        response = self.get_url(url=f"{self.base_url}/indexer", params={})

        if response.status_code == 200:
            indexers_list = response.json()
            return [Indexer(**indexer) for indexer in indexers_list]
        else:
            return [Indexer]

    def get_torrent_url(self, url: str, filename: str):

        response = self.get_url(url=url)
        if response.status_code == 200:
            # Write the torrent to file
            with open(os.path.join(config_settings.options.PW_TORRENT_ARCHIVE_PATH,f"{filename}.torrent"), 'wb') as f:
                f.write(response.content)

    def search(self, query: str) -> list[Search] | None:
        """Get search queue."""

        params = {"query": query}
        url = f"{self.base_url}/search?"

        response = self.get_url(url=url, params=params)
        if response:
            if response.status_code == 200:
                results_list = response.json()
                return [Search(**result) for result in results_list]
            else:
                return []
        return None

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
