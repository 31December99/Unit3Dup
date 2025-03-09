# -*- coding: utf-8 -*-
import os
import re

from common.external_services.igdb.core.tags import (
    crew_patterns,
    additions,
    platform_patterns,
)
from common.utility import ManageTitles, System
from common.mediainfo import MediaFile
from common import title

from view import custom_console

class Media:
    def __init__(self, folder: str, subfolder: str):
        self.folder: str = folder
        self.subfolder: str = subfolder
        self.title = os.path.basename(os.path.join(self.folder, self.subfolder))

        # // Media
        self._crew_list: list[str] | None = None
        self._platform_list: list[str] | None = None
        self._title_sanitized: str | None = None
        self._guess_title: str | None = None
        self._guess_filename: str | None = None
        self._guess_season: int | None = None
        self._episode: str | None = None
        self._source: str | None = None
        self._screen_size: int | None = None
        self._audio_codec: str | None = None
        self._subtitle: str | None = None
        self._torrent_path: str | None = None

        # // Contents
        self._file_name: str | None = None
        self._display_name: str | None = None
        self._category: int | None = None
        self._audio_languages: list[str] | None = None
        self._media_file: MediaFile | None = None
        self._languages: list[str] | None = None
        self._resolution: int | None = None
        self._tracker_name: str | None = None

        # // Contents dall'esterno
        self._torrent_name: str | None = None
        self._size: int = 0
        self._metainfo: str | None = None
        self._torrent_pack: bool = False
        self._doc_description: str | None = None
        self._game_nfo: str | None = None

    @property
    def title_sanitized(self)-> str:
        if not self._title_sanitized:
            self._title_sanitized = self._filename_sanitized_()
        return self._title_sanitized

    @title_sanitized.setter
    def title_sanitized(self, value):
        self.title_sanitized = value

    @property
    def crew_list(self) -> list['str']:
        if not self._crew_list:
            self._crew_list = self._crew(filename=self.title_sanitized)
        return self._crew_list

    @property
    def platform_list(self) -> list['str']:
        if not self._platform_list:
            self._platform_list = self._platform(filename=self.title_sanitized)
        return self._platform_list


    @property
    def torrent_name(self)-> str:
        return self._torrent_name

    @torrent_name.setter
    def torrent_name(self, value):
        self._torrent_name = value

    @property
    def size(self)-> int:
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def metainfo(self)-> str:
        return self._metainfo

    @metainfo.setter
    def metainfo(self, value):
        self._metainfo = value

    @property
    def doc_description(self) -> str:
        return self._doc_description

    @doc_description.setter
    def doc_description(self, value):
        self._doc_description = value

    @property
    def tracker_name(self) -> str:
        return self._tracker_name

    @tracker_name.setter
    def tracker_name(self, value):
        self._tracker_name = value

    @property
    def torrent_pack(self) -> bool:
        return self._torrent_pack

    @torrent_pack.setter
    def torrent_pack(self, value):
        self._torrent_pack = value

    @property
    def game_nfo(self) -> str:
        return self._game_nfo

    @game_nfo.setter
    def game_nfo(self, value):
        self._game_nfo = value

    @property
    def guess_filename(self):
        if not self._guess_filename:
            self._guess_filename = title.Guessit(self.title_sanitized)
        return self._guess_filename

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self,value):
        self._file_name = value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value
        if self._display_name:
            episode_title = self.guess_filename.guessit_episode_title
            if episode_title:
                self._display_name = " ".join(
                    self._display_name.replace(episode_title, "").split()
                )

    @property
    def guess_title(self)-> str:
        if not self._guess_title:
            self._guess_title = title.Guessit(self.title_sanitized).guessit_title
        return self._guess_title

    @property
    def guess_season(self):
        if not self._guess_season:
            self._guess_season = self.guess_filename.guessit_season
        return self._guess_season

    @property
    def guess_episode(self):
        if not self._episode:
            self._episode = self.guess_filename.guessit_episode
        return self._episode

    @property
    def source(self):
        if not self._source:
            self._source = self.guess_filename.source
        return self._source


    @property
    def screen_size(self):
        if not self._screen_size:
            screen_split = self.title_sanitized.split(" ")
            for screen in screen_split:
                if screen in System.RESOLUTION_labels:
                    self._screen_size = screen
        return self._screen_size


    @property
    def audio_codec(self):
        if not self._audio_codec:
            self._audio_codec = self.guess_filename.audio_codec
        return self._audio_codec


    @property
    def audio_languages(self):
        if not self._audio_languages:
            # Get languages from the title
            filename_split = self.display_name.upper().split(" ")
            for code in filename_split:
                if converted_code := ManageTitles.convert_iso(code):
                    self._audio_languages = [converted_code]
                    return self._audio_languages
        return self._audio_languages

    @property
    def subtitle(self):
        if not self._subtitle:
            self._subtitle = self.guess_filename.subtitle
        return self._subtitle

    @property
    def torrent_path(self) -> str:
        if not self._torrent_path:
            self._torrent_path = os.path.join(self.folder, self.subfolder)
        return self._torrent_path


    @property
    def category(self):
        if self._category:
            return self._category

        # Check for ext file
        if ManageTitles.media_docu_type(self.title):
            self._category = System.category_list.get(System.DOCUMENTARY)
            # Check for season
        elif self.guess_filename.guessit_season:
            self._category = System.category_list.get(System.TV_SHOW)
        # it's a movie
        else:
            self._category = System.category_list.get(System.MOVIE)

        # If there's a crew or platform list -> game
        if self.crew_list or self.platform_list:
            self._category = System.category_list.get(System.GAME)
        return self._category

    @property
    def game_title(self):
        return self.guess_filename.guessit_title

    @property
    def mediafile(self):
        if not self._media_file:
            if self.category in {
                System.category_list.get(System.MOVIE),
                System.category_list.get(System.TV_SHOW),
            }:
                # Read from the current video file the height field
                file_path = os.path.join(self.folder, self.file_name)

                # Media file
                self._media_file = MediaFile(file_path)
        return self._media_file

    @property
    def languages(self):
        if not self._languages:
            self._languages = self.mediafile.available_languages
        return self._languages


    @property
    def resolution(self):
        if not self._resolution:
            if self.mediafile:
                # The resolution from the mediainfo not always mach those in tracker data
                # so we apply the difference between 'x' (tracker resolution in set) and the video_height
                # do it for each value in resolution_values and return the min among all values
                # example: height = 1000...
                # For 720: abs(720 - 1000) = 280
                # For 1080: abs(1080 - 1000) = 80
                # -> get 1080

                if self.mediafile.video_height:
                    closest_resolution = min(
                        System.RESOLUTIONS,
                        key=lambda x: abs(int(x) - int(self.mediafile.video_height)),
                    )

                    # Get scan type: progressive or interlaced
                    scan_type = self.mediafile.video_scan_type

                    if scan_type:
                        if scan_type.lower() == "progressive":
                            closest_resolution = f"{closest_resolution}p"
                        else:
                            closest_resolution = f"{closest_resolution}i"
                    else:
                        # else read the interlaced field..
                        if self.mediafile.is_interlaced:
                            closest_resolution = f"{closest_resolution}i"
                        else:
                            closest_resolution = f"{closest_resolution}p"

                    self._resolution = closest_resolution
                else:
                    custom_console.bot_error_log(
                        f"'{self.__class__.__name__}' Video Height resolution not found in {self.file_name}"
                    )
                    custom_console.bot_error_log(
                        f"'{self.__class__.__name__}' Set to default value {System.NO_RESOLUTION}"
                    )
                    self._resolution = System.NO_RESOLUTION
            else:
                # Game
                self._resolution = System.NO_RESOLUTION
        return self._resolution

    def _filename_sanitized_(self):
        # Basename of the content path
        filename_sanitized = self.title
        # Remove each addition from the string
        for addition in additions:
            filename_sanitized = re.sub(
                rf"\b{addition}\b", "", filename_sanitized
            )

        # Remove v version
        filename_sanitized = re.sub(
            r"v\d+(?:[ .]\d+)*", "", filename_sanitized
        ).strip()

        # Remove dots, hyphens and extra spaces
        filename_sanitized = re.sub(
            r"[.\-_]", " ", filename_sanitized
        ).strip()
        filename_sanitized = re.sub(r"\s+", " ", filename_sanitized)

        # Remove flag
        filename_sanitized = re.sub(r'\b(ita|eng)\b', ' ', filename_sanitized, flags=re.IGNORECASE)
        return filename_sanitized


    @staticmethod
    def _crew(filename: str)-> list[str]:
        # Get the crew name only if the substr is at end of the string
        crew_regex = (
                r"\b(" + "|".join(re.escape(pattern) for pattern in crew_patterns) + r")\b$"
        )
        return re.findall(crew_regex, filename, re.IGNORECASE)

    @staticmethod
    def _platform(filename: str) -> list[str]:

        # Get the platform name
        platform_regex = (
                r"\b("
                + "|".join(re.escape(pattern) for pattern in platform_patterns)
                + r")\b"
        )
        platform_list = re.findall(platform_regex, filename, re.IGNORECASE)

        # Remove the platform string from the name
        return platform_list