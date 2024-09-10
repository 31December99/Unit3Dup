import os
from dataclasses import dataclass


@dataclass
class Contents:
    """Create a new object with the attributes of Contents"""

    file_name: str
    folder: str
    name: str
    size: int
    metainfo: str
    category: int
    tracker_name: str
    torrent_pack: bool
    torrent_path: str
    display_name: str
    doc_description: str
    audio_languages: list[str]


@dataclass
class Media:
    """

    For each Folder, create an object with attributes:
    folder, subfolder, media_type, other, audio_codec, subtitle, resolution

    """

    folder: str
    subfolder: str
    media_type: str
    source: str
    other: str
    audio_codec: str
    subtitle: str
    resolution: str

    @property
    def torrent_path(self) -> str:
        return os.path.join(self.folder, self.subfolder)
