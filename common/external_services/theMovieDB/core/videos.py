# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class Videos:
    id: str
    iso_3166_1: str
    iso_639_1: str
    key: str
    name: str
    official: bool
    published_at: str
    site: str
    size: int
    type: str

@dataclass
class Data:
    id: int
    results: list[Videos]
