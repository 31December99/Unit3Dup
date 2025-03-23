# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC
from dataclasses import dataclass, field


class Media(ABC):

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_original(self) -> str:
        pass


@dataclass
class TvShow(Media):
    """
    A tv object for the search endpoint
    """

    id: int
    name: str
    first_air_date: str
    overview: str
    popularity: float
    vote_average: float
    vote_count: int
    genre_ids: list[int] = field(default_factory=list)
    origin_country: list[str] = field(default_factory=list)
    original_language: str = ''
    original_name: str = ''
    backdrop_path: str | None = None
    poster_path: str | None = None
    adult: bool = False

    def get_title(self) -> str:
        return self.name

    def get_original(self) -> str:
        return self.original_name