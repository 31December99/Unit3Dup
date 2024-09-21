# -*- coding: utf-8 -*-
from dataclasses import dataclass


# 05/09/2024
# Automatically creates __init__, __repr__, and other methods
#
@dataclass(frozen=True)
class OnTheAir:
    adult: bool | None = None
    backdrop_path: str | None = None
    genre_ids: list[int] | None = None
    id: int | None = None
    original_language: str | None = None
    original_title: str | None = None
    overview: str | None = None
    popularity: float | None = None
    poster_path: str | None = None
    release_date: str | None = None
    title: str | None = None
    video: bool | None = None
    vote_average: float | None = None
    vote_count: int | None = None
    origin_country: list[str] | None = None
    original_name: str | None = None
    first_air_date: str | None = None
    name: str | None = None
