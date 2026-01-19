import tvdb_v4_official
from common.utility import ManageTitles
from unit3dup import config_settings


class TVDB:

    def __init__(self, category: str):
        self.api = tvdb_v4_official.TVDB(config_settings.tracker_config.TVDB_APIKEY)
        self.category = category
        self.filtered_results = []

    def search(self, query: str) -> int | None:
        results = self.api.search(query=query)

        if 'tv' in self.category.lower():
            self.filtered_results = [item for item in results if item['type'] == 'series']
        elif 'movie' in self.category.lower():
            self.filtered_results = [item for item in results if item['type'] == 'movie']

        for item in self.filtered_results:
            title = item.get('name', '') or item.get('extended_title', '')
            score = ManageTitles.fuzzyit(str1=query, str2=title)
            if score > 95:
                return item.get('tvdb_id')
        return None
