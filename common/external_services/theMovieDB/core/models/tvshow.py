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

    def __repr__(self) -> str:
        """
        Provides a string representation of the TvShow object.

        Returns:
            str: A string representation of the TV show object.
        """
        return f"TvShow(id={self.id}, name='{self.name}', first_air_date='{self.first_air_date}')"
