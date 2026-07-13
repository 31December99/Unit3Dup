# -*- coding: utf-8 -*-

from datetime import datetime

class MediaResult:
    def __init__(self, result=None, video_id: int = 0, imdb_id = None, tvdb_id = None, trailer_key: str = None,
                 keywords_list: str = None, season_title = None):
        self.result = result
        self.trailer_key = trailer_key
        self.keywords_list = keywords_list
        self.video_id = video_id
        self.imdb_id = imdb_id
        self.tvdb_id = tvdb_id
        self.season_title = season_title
        self.year = None

        if result:
            try:
                self.year = datetime.strptime(result.get_date(), '%Y-%m-%d').year
            except ValueError:
                pass




