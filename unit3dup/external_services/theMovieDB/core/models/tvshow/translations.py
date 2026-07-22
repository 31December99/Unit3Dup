# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any


@dataclass
class TvTranslationData:
    homepage: str | None = None
    overview: str | None = None
    tagline: str | None = None
    name: str | None = None

    @staticmethod
    def from_data(data: dict[str, Any]) -> "TvTranslationData":
        return TvTranslationData(
            homepage=data.get("homepage"),
            overview=data.get("overview"),
            tagline=data.get("tagline"),
            name=data.get("name"),
        )


@dataclass
class TvTranslation:
    iso_3166_1: str
    iso_639_1: str
    name: str
    english_name: str
    data: TvTranslationData | None = None

    @staticmethod
    def from_data(data: dict[str, Any]) -> "TvTranslation":
        return TvTranslation(
            iso_3166_1=data["iso_3166_1"],
            iso_639_1=data["iso_639_1"],
            name=data["name"],
            english_name=data["english_name"],
            data=TvTranslationData.from_data(data.get("data", {})) if data.get("data") else None,
        )

@dataclass
class Translation:
    id: int
    translations: list[TvTranslation]