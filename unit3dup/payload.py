# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from common.utility import title, utility
from media_db import results


@dataclass
class Data:
    metainfo: str
    name: str
    file_name: str
    result: results
    category: int
    standard: int
    media_info: str
    description: str
    myguess: title.Guessit = field(init=False)
    igdb: int
    platform: str

    def __post_init__(self):
        self.name = utility.ManageTitles.clean(self.name)
        self.myguess = title.Guessit(self.file_name)  #.guessit_title
