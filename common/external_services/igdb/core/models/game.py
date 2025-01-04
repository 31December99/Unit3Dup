# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class Game:
    id: int
    name: str
    summary: str
    videos: list
    description: str = field(init=False)
