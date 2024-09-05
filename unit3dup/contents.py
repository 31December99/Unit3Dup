import os
from dataclasses import dataclass


@dataclass
class Contents:
    """Create a new object with the attributes of Contents"""

    file_name: str
    folder: str
    name: str
    size: int
    metainfo: dict[str, any]
    category: int
    tracker_name: str
    torrent_pack: bool
    torrent_path: str
    display_name: str
    doc_description: str
    audio_languages: list[str]


@dataclass
class File:
    """
    For each File, create an object with attributes:
    file_name, folder, media_type, torrent_name, source, other, audio_codec, subtitle, resolution
    """

    file_name: str
    folder: str
    media_type: str
    torrent_name: str
    source: str
    other: str
    audio_codec: str
    subtitle: str
    resolution: str

    @property
    def torrent_path(self) -> str:
        return os.path.join(self.folder, self.file_name)


@dataclass
class Folder:
    """

    For each Folder, create an object with attributes:
    folder, subfolder, media_type, torrent_name, source, other, audio_codec, subtitle, resolution

    """

    folder: str
    subfolder: str
    media_type: str
    torrent_name: str
    source: str
    other: str
    audio_codec: str
    subtitle: str
    resolution: str

    @property
    def torrent_path(self) -> str:
        return os.path.join(self.folder, self.subfolder)
