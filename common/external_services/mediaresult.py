# -*- coding: utf-8 -*-

class MediaResult:
    def __init__(self, result=None, video_id: int = 0, imdb_id = None, trailer_key: str = None, keywords_list: str = None):
        self.result = result
        self.trailer_key = trailer_key
        self.keywords_list = keywords_list
        self.video_id = video_id
        self.imdb_id = imdb_id

