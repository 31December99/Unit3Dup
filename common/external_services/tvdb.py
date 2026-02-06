import tvdb_v4_official
from common.utility import ManageTitles
from unit3dup import config_settings


class TVDB:

    def __init__(self, category: str):
        self.api = tvdb_v4_official.TVDB(config_settings.tracker_config.TVDB_APIKEY)
        self.category = category
        self.filtered_results = []

    def search(self, query: str) -> dict | None:
        show_type=''
        if self.category == "tv":
            show_type='series'
        if self.category == "movie":
            show_type='movie'
        results = self.api.search(query=query, type=show_type)
        self.filtered_results = [item for item in results]
        for item in self.filtered_results:
            title = item.get('name', '') or item.get('extended_title', '')
            translations = item.get('translations', [])
            remote_ids = item.get('remote_ids', [])
            imdb_id = None
            for remote_id in remote_ids:
                if 'IMDB' in remote_id.get('sourceName').upper():
                    imdb_id = remote_id.get('id').lower().replace('tt', '')
            score = ManageTitles.fuzzyit(str1=query, str2=title)
            if score > 95:
                return {'tvdb_id' : item.get('tvdb_id'), 'imdb_id': imdb_id}
            if translations:
                title_ita = translations.get('ita', None)
                if title_ita:
                    score = ManageTitles.fuzzyit(str1=query, str2=title_ita)
                    if score > 95:
                        return {'tvdb_id': item.get('tvdb_id'), 'imdb_id': imdb_id}

        return None
