from dataclasses import dataclass


@dataclass
class Search:
    """
    Get a result from the endpoint /search?query

    """
    age: int = 0
    ageHours: float = 0.0
    ageMinutes: float = 0.0
    categories: list[dict[str, any]] = None
    downloadUrl: str = ""
    fileName: str = ""
    guid: str = ""
    imdbId: int = 0
    indexer: str = ""
    indexerFlags: list[str] = None
    indexerId: int = 0
    infoUrl: str = ""
    leechers: int = 0
    protocol: str = "torrent"
    publishDate: str = ""
    seeders: int = 0
    size: int = 0
    sortTitle: str = ""
    title: str = ""
    tmdbId: int = 0
    tvMazeId: int = 0
    tvdbId: int = 0
