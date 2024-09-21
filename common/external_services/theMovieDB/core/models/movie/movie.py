# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Movie:
    """
    A movie object for the search endpoint
    """
    adult: bool
    backdrop_path: str
    genre_ids: list[int]
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str
    title: str
    video: bool
    vote_average: float
    vote_count: int
