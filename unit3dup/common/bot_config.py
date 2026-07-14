# -*- coding: utf-8 -*-

from dataclasses import dataclass, fields


@dataclass(slots=True)
class BotConfig:
    # Config commands
    # check: bool = False

    # Upload commands
    upload: str | None = None
    mode: str | None = None
    folder: str = None
    scan: str | None = None
    buildtags: bool = False
    reseed: bool = False
    watcher: bool = False
    notitle: str | None = None

    tracker: str = "itt"
    mt: bool = False
    force: str | None = None

    noseed: bool = False
    noup: bool = False
    duplicate: bool = False
    personal: bool = False
    ftp: bool = False

    # Search commands
    dump: bool = False
    search: str | None = None
    dbsave: bool = False
    info: str | None = None
    uploader: str | None = None
    description: str | None = None
    bdinfo: str | None = None
    mediainfo: str | None = None
    internal: bool = False
    moderation: bool = False

    # Filters
    startyear: str | None = None
    endyear: str | None = None
    type: str | None = None
    resolution: str | None = None
    filename: str | None = None
    season: str | None = None
    episode: str | None = None

    # IDs
    tmdb_id: str | None = None
    imdb_id: str | None = None
    tvdb_id: int | None = None
    mal_id: str | None = None
    playlist_id: str | None = None
    collection_id: str | None = None

    # Status
    freelech: str | None = None
    alive: bool = False
    dead: bool = False
    dying: bool = False

    # Special flags
    doubleup: bool = False
    featured: bool = False
    refundable: bool = False
    stream: bool = False
    standard: bool = False
    highspeed: bool = False
    intern_r: bool = False
    prelease: bool = False

    # xxxx
    is_dir: bool | None = None

    @classmethod
    def from_namespace(cls, namespace):
        data = vars(namespace)

        valid_fields = {
            field.name
            for field in fields(cls)
        }

        filtered_data = {
            key: value
            for key, value in data.items()
            if key in valid_fields
        }

        return cls(**filtered_data)
