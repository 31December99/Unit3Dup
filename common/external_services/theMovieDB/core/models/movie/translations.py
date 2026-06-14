# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

#Movie
@dataclass
class TranslationData:
    homepage: str | None = None
    overview: str | None = None
    runtime: int | None = None
    tagline: str | None = None
    title: str | None = None
    name: str | None = None


@dataclass
class Translation:
    iso_3166_1: str
    iso_639_1: str
    name: str
    english_name: str
    data: TranslationData | dict

    def __post_init__(self):
        if isinstance(self.data, dict):
            self.data = TranslationData(**self.data)


@dataclass
class TranslationsResponse:
    id: int
    translations: List[Translation]