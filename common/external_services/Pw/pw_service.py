# -*- coding: utf-8 -*-

from common.external_services.Pw.core.pw_api import PwAPI
from common.external_services.Pw.core.models.indexers import Indexer
from common.external_services.Pw.core.models.search import Search


class PwService:

    def __init__(self):
        self.pw_api = PwAPI()

    def get_indexers(self) -> ['Indexer']:
        return self.pw_api.get_indexers()

    def search(self, query: str) -> ['Search']:
        return self.pw_api.search(query=query)
