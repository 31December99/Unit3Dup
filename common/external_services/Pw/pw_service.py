# -*- coding: utf-8 -*-

from common.external_services.Pw.core.pw_api import PwAPI
from common.external_services.Pw.core.models.indexers import Indexer
from common.external_services.Pw.core.models.search import Search
from common.external_services.Pw.core.models.torrent_client_config import TorrentClientConfig


class PwService:

    def __init__(self):
        self.pw_api = PwAPI()

    async def init(self):
        await self.pw_api.init_session()

    async def get_indexers(self) -> [Indexer]:
        return await self.pw_api.get_indexers()

    async def search(self, query: str) -> list[Search]:
        return await self.pw_api.search(query=query)

    async def get_torrent_client_ids(self) -> list[TorrentClientConfig]:
        return await self.pw_api.get_torrent_client_ids()

    async def send_torrent_to_client(self, payload):
        return await self.pw_api.send_torrent_to_client(payload)

    async def close(self):
        await self.pw_api.close()



