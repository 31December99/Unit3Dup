# -*- coding: utf-8 -*-

from common.external_services.theMovieDB.core.api import MediaResult
from dataclasses import dataclass, field
from common.utility import title, utility

@dataclass
class Data:
    metainfo: str
    name: str
    file_name: str
    show: MediaResult | None
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
