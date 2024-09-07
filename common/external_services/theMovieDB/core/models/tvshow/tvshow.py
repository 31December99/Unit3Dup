# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class TvShow:
    """
    Represents a TV show.
    """

    id: int
    name: str
    first_air_date: str
    overview: str
    popularity: float
    vote_average: float
    vote_count: int
    genre_ids: list[int]
    origin_country: list[str]
    original_language: str
    original_name: str
    backdrop_path: str | None = None
    poster_path: str | None = None
    adult: bool = False
