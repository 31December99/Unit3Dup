import os
import re

from common.trackers.trackers import ITTData
from dataclasses import dataclass, field
from common.mediainfo import MediaFile
from common.utility import title

crew_pattern = (
    r"\b("
    # Nintendo Switch
    r"NSW-(VENOM|nogrp|LiGHTFORCE|SUXXORS|HR|NiiNTENDO|GANT|BREWS)|"
    # PC
    r"REPACK-Kaos|GOG|TENOKE|rG|I\sKnow|Razor1911|RUNE|FitGirl\sRepack|DODI\sRepack|ElAmigos|"
    r"RazorDOX|RAZOR|SKIDROW|DINOByTES|TiNYiSO|FCKDRM|FLT|Unleashed|"
    # PS4 e PS5
    r"PS4|PS5|"
    r"I_KnoW)\b"
)

tag_pattern = (
    r"\b(PC|WIN|WIN32|WIN64|LIN|LNX|MAC|OSX|XBOX|X360|XONE|XBO|XSX|XSS|PS1|PSX|PS2|PS3|PS4|PS5|PSP|PSV|NES"
    r"|SNES|N64|GC|NGC|WII|WIIU|NS|SWITCH|3DS|NDS|DS|GEN|MD|SAT|DC|GB|GBC|GBA|ANDROID|IOS|STADIA|LUNA|VR"
    r"|RIFT|VIVE|DLC|Linux)\b"
)


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
    game_title: str
    game_crew: list

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
            self.resolution = tracker_data.resolution["altro"]
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

    @property
    def guess_filename(self):
        temp_name = os.path.basename(self.subfolder)
        temp_name = temp_name.replace(".", " ")
        for crew_name in self.crew:
            temp_name = temp_name.replace(crew_name, "")

        for tag_name in self.tags:
            temp_name = temp_name.replace(tag_name, "")
        return title.Guessit(temp_name)

    @property
    def source(self):
        return self.guess_filename.source

    @property
    def other(self):
        return self.guess_filename.other

    @property
    def audio_codec(self):
        return self.guess_filename.audio_codec

    @property
    def subtitle(self):
        return self.guess_filename.subtitle

    @property
    def resolution(self):
        return self.guess_filename.screen_size

    @property
    def torrent_path(self) -> str:
        return os.path.join(self.folder, self.subfolder)

    @property
    def crew(self) -> list:
        matches = re.findall(crew_pattern, self.subfolder, re.IGNORECASE)
        extracted_tags = [match[0] for match in matches]
        return extracted_tags

    @property
    def tags(self) -> list:
        matches = re.findall(tag_pattern, self.subfolder, re.IGNORECASE)
        return matches

    @property
    def media_type(self):

        tracker_data = ITTData.load_from_module()
        movie_category = tracker_data.category.get("movie")
        serie_category = tracker_data.category.get("tvshow")
        game_category = tracker_data.category.get("game")

        if self.guess_filename.guessit_season:
            media_type = serie_category
        else:
            media_type = movie_category
        if self.crew:
            media_type = game_category
        return media_type

    @property
    def game_title(self):
        return self.guess_filename.guessit_title
