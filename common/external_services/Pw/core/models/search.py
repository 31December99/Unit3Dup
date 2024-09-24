# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class Search:
    """
    Get a result from the endpoint /search?query

    """

    age: int = 0
    ageHours: float = 0.0
    ageMinutes: float = 0.0
    categories: list[dict[str, any]] = field(default_factory=list)
    downloadUrl: None | str = None
    fileName: None | str = None
    guid: None | str = None
    imdbId: int = 0
    indexer: None | str = None
    indexerFlags: list[str] = field(default_factory=list)
    indexerId: int = 0
    infoUrl: None | str = None
    leechers: int = 0
    protocol: str = "torrent"
    publishDate: None | str = None
    seeders: int = 0
    size: int = 0
    sortTitle: None | str = None
    title: None | str = None
    tmdbId: int = 0
    tvMazeId: int = 0
    tvdbId: int = 0
