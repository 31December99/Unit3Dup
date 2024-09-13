import os
from dataclasses import dataclass, field
from common.utility import title


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
    episode_title: str = field(init=False)

    def __post_init__(self):
        guess_filename = title.Guessit(self.file_name)
        self.episode_title = guess_filename.guessit_episode_title


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
