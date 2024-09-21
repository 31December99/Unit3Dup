# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class Results:
    """

    Contains the result of the TMDB search

    """

    genre_ids: list[int] | None = None
    popularity: list[float] | None = None
    overview: str | None = None
    result: str | None = None
    video_id: int = 0
    alternative: list[str] = field(default_factory=list)
    translations: list[str] = field(default_factory=list)
    poster_path: list[str] = field(default_factory=list)
    backdrop_path: list[str] = field(default_factory=list)
    genres_id: list[int] | None = None
    title: str | None = None
    original_title: str | None = None
    date: str | None = None
    not_resources: bool = False
    keywords: bool = False
