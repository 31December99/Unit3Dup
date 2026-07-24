# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class Alternative:
    iso_3166_1: str
    title: str
    type: str

@dataclass
class DataResponse:
    id: int
    results: list[Alternative]
