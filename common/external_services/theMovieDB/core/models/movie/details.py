# -*- coding: utf-8 -*-

# Tempus fugit

from dataclasses import dataclass
from abc import ABC, abstractmethod

class Media(ABC):

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_original(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass

@dataclass
class Genre:
    id: int
    name: str

@dataclass
class ProductionCompany:
    id: int
    logo_path: str | None
    name: str
    origin_country: str

@dataclass
class ProductionCountry:
    iso_3166_1: str
    name: str

@dataclass
class SpokenLanguage:
    english_name: str
    iso_639_1: str
    name: str

@dataclass
class MovieDetails(Media):
    adult: bool
    backdrop_path: str | None
    belongs_to_collection: str | None
    budget: int
    genres: list[Genre]
    homepage: str
    id: int
    imdb_id: str
    origin_country: list[str]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str | None
    production_companies: list[ProductionCompany]
    production_countries: list[ProductionCountry]
    release_date: str
    revenue: int
    runtime: int
    spoken_languages: list[SpokenLanguage]
    status: str
    tagline: str
    title: str
    video: bool
    vote_average: float
    vote_count: int

    def get_title(self) -> str:
        return self.title

    def get_original(self) -> str:
        return self.original_title

    def get_date(self) -> str:
        return self.release_date
