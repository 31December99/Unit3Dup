# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


# Tempus fugit

@dataclass
class CreatedBy:
    credit_id: str
    gender: int
    id: int
    name: str
    original_name: str
    profile_path: str | None = None


@dataclass
class Genre:
    id: int
    name: str


@dataclass
class LastEpisodeToAir:
    air_date: str
    episode_number: int
    episode_type: str
    id: int
    name: str
    overview: str
    production_code: str
    runtime: int
    season_number: int
    show_id: int
    vote_average: float
    vote_count: int
    still_path: str | None = None


@dataclass
class Network:
    id: int
    logo_path: str
    name: str
    origin_country: str


@dataclass
class ProductionCompany:
    id: int
    name: str
    origin_country: str
    logo_path: str | None = None


@dataclass
class ProductionCountry:
    iso_3166_1: str
    name: str


@dataclass
class Season:
    episode_count: int
    id: int
    name: str
    overview: str
    season_number: int
    vote_average: float
    air_date: str | None = None
    poster_path: str | None = None


@dataclass
class SpokenLanguage:
    english_name: str
    iso_639_1: str
    name: str


@dataclass
class TVShowDetails:
    adult: bool
    first_air_date: str
    homepage: str
    id: int
    in_production: bool
    last_air_date: str
    last_episode_to_air: LastEpisodeToAir
    name: str
    number_of_episodes: int
    number_of_seasons: int
    original_language: str
    original_name: str
    overview: str
    popularity: float
    poster_path: str
    status: str
    tagline: str
    type: str
    vote_average: float
    vote_count: int
    languages: list[str] = field(default_factory=list)
    genres: list[Genre] = field(default_factory=list)
    backdrop_path: str | None = None
    created_by: list[CreatedBy] = field(default_factory=list)
    episode_run_time: list[int] = field(default_factory=list)
    networks: list[Network] = field(default_factory=list)
    next_episode_to_air: LastEpisodeToAir | None = None
    production_companies: list[ProductionCompany] = field(default_factory=list)
    production_countries: list[ProductionCountry] = field(default_factory=list)
    seasons: list[Season] = field(default_factory=list)
    spoken_languages: list[SpokenLanguage] = field(default_factory=list)
    origin_country: list[str] = field(default_factory=list)
