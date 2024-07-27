# -*- coding: utf-8 -*-
from unit3dup import results, utility, title



class Data:

    def __init__(self, metainfo: str, name: str, file_name: str, result: results, category: int, standard: int,
                 mediainfo: str, description: str):
        self.metainfo = metainfo
        self.name = utility.Manage_titles.clean(name)
        self.file_name = file_name
        self.myguess = title.Guessit(file_name)
        self.result = result
        self.category = category
        self.standard = standard
        self.media_info = mediainfo
        self.description = description

    @classmethod
    def create_instance(cls, metainfo: str, name: str, file_name: str, result: results, category: int, standard: int,
                        mediainfo: str, description: str):
        return cls(metainfo, name, file_name, result, category, standard, mediainfo, description)
