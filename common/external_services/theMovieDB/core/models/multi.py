from dataclasses import dataclass, field
from typing import List, Optional
from abc import ABC, abstractmethod

class Media(ABC):

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> int:
        pass


@dataclass
class Movie(Media):
    backdrop_path: str
    id: int
    title: str
    original_title: str
    overview: str
    poster_path: str
    media_type: str
    adult: bool
    original_language: str
    genre_ids: List[int]
    popularity: float
    release_date: str
    video: bool
    vote_average: float
    vote_count: int
    keywords: str = field(init=False, default_factory=str)
    trailer_code: str = field(init=False, default_factory=str)


    def get_title(self) -> str:
        return self.title

    def get_id(self) -> int:
        return self.id


@dataclass
class TVShow(Media):
    backdrop_path: Optional[str]
    id: int
    name: str
    original_name: str
    overview: str
    poster_path: Optional[str]
    media_type: str
    adult: bool
    original_language: str
    genre_ids: List[int]
    popularity: float
    first_air_date: str
    vote_average: float
    vote_count: int
    origin_country: List[str]
    keywords: str = field(init=False, default_factory=str)
    trailer_code: str = field(init=False, default_factory=str)

    def get_title(self) -> str:
        return self.name

    def get_id(self) -> int:
        return self.id

