# -*- coding: utf-8 -*-

from common.external_services.theMovieDB.core.models.multi import Movie, TVShow
from dataclasses import dataclass, field
from common.utility import title, utility

@dataclass
class Data:
    metainfo: str
    name: str
    file_name: str
    show: Movie | TVShow | None
    category: int
    standard: int
    media_info: str
    description: str
    myguess: title.Guessit = field(init=False)
    igdb: int
    platform: str

    def __post_init__(self):
        self.name = utility.ManageTitles.clean(self.name)
        self.myguess = title.Guessit(self.file_name)
