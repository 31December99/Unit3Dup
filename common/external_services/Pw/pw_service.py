# -*- coding: utf-8 -*-

from common.external_services.Pw.core.pw_api import PwAPI
from common.external_services.Pw.core.models.indexers import Indexer
from common.external_services.Pw.core.models.search import Search
from common.external_services.Pw.core.models.torrent_client_config import TorrentClientConfig


class PwService:

    def __init__(self):
        self.pw_api = PwAPI()

    def get_indexers(self) -> [Indexer]:
        return self.pw_api.get_indexers()

    def search(self, query: str) -> list[Search]:
        return self.pw_api.search(query=query)

    def get_torrent_client_ids(self) -> list[TorrentClientConfig]:
        return self.pw_api.get_torrent_client_ids()

    def send_torrent_to_client(self, payload):
        return self.pw_api.send_torrent_to_client(payload)

    def get_torrent_from_pw(self, torrent_url: str, download_filename: str)-> str | None:
        response = self.pw_api.get_torrent_url(url=torrent_url, filename=download_filename)
        # Redirect (PW)
        if response.status_code == 301:
            return response.headers.get('Location')
        return None



