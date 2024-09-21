import os
from common.trackers.trackers import ITTData
from dataclasses import dataclass, field
from common.mediainfo import MediaFile
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
    resolution: int = field(init=False)

    def __post_init__(self):
        # Search for the episode title
        guess_filename = title.Guessit(self.file_name)
        self.episode_title = guess_filename.guessit_episode_title
        if self.episode_title:
            self.display_name = " ".join(
                self.display_name.replace(self.episode_title, "").split()
            )

        # Search for resolution based on mediainfo string
        tracker_data = ITTData.load_from_module()
        file_path = os.path.join(self.folder, self.file_name)
        media_file = MediaFile(file_path)
        video_height = f"{media_file.video_height}p"
        if video_height not in tracker_data.resolution:
            self.resolution = tracker_data.resolution['altro']
        else:
            self.resolution = tracker_data.resolution[video_height]


@dataclass
class Media:
    """

    For each Folder, create an object with attributes:
    folder, subfolder, media_type, other, audio_codec, subtitle, resolution

    """

    folder: str
    subfolder: str
    media_type: int
    source: str
    other: str
    audio_codec: str
    subtitle: str
    resolution: str

    @property
    def torrent_path(self) -> str:
        return os.path.join(self.folder, self.subfolder)
