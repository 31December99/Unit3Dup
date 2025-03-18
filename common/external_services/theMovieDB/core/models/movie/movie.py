# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from abc import ABC, abstractmethod

class Media(ABC):

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_original(self) -> str:
        pass

@dataclass
class Movie(Media):
    """
    A movie object for the search endpoint
    """
    adult: bool = False
    backdrop_path: str = ''
    genre_ids: list[int] = field(default_factory=list)
    id: int = 0
    original_language: str = ''
    original_title: str = ''
    overview: str = ''
    popularity: float = 0.0
    poster_path: str = ''
    release_date: str = ''
    title: str = ''
    video: bool = False
    vote_average: float = 0.0
    vote_count: int = 0

    def get_title(self) -> str:
        return self.title

    def get_original(self) -> str:
        return self.original_title