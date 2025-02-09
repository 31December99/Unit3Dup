# -*- coding: utf-8 -*-
import json
import os
import re

from unit3dup.contents import Contents
from unit3dup.contents import Media
from unit3dup.automode import Auto

from common.trackers.trackers import ITTData
from common.utility import ManageTitles

class ContentManager:
    def __init__(self, path: str, tracker_name: str, mode: str, force_media_type=None):
        """
        Args:
            path (str): The path to the media files or directories
            tracker_name (str): The tracker name for the content
            mode (str):  mode 'manual' or 'automatic'
            force_media_type: if the -serie, -movie, -game si active
        """
        self.path = path
        self.tracker_name = tracker_name
        self.mode = mode
        self.force_media_type = force_media_type

        self.languages: list[str] | None = None
        self.display_name: str | None = None
        self.meta_info_list: list[dict] = []
        self.game_nfo: str = ''
        self.category: int | None = None

        self.meta_info: str | None = None
        self.size: int | None = None
        self.torrent_name: str | None = None
        self.folder: str | None = None
        self.file_name: str | None = None
        self.torrent_path: str | None = None
        self.doc_description: str | None = None

        self.tracker_name: str = tracker_name
        self.path: str = os.path.normpath(path)
        self.tracker_data = ITTData.load_from_module()

        self.auto = Auto(path=self.path, mode=self.mode, tracker_name=self.tracker_name,
                         force_media_type=self.force_media_type)
        self.media_list = self.auto.upload() if self.mode in ["man", "folder"] else self.auto.scan()

    def process(self)-> list['Contents']:
        contents = []
        for media in self.media_list:
            self.path = media.torrent_path
            self.category = media.media_type

            content = self.get_data(media=media)
            if content:
                contents.append(content)
        return contents

    def get_data(self, media: Media) -> Contents | bool:
        """
        Process files or folders and create a `Contents` object if the metadata is valid
        """

        if os.path.isdir(self.path):
            self.process_folder()
        elif os.path.isfile(self.path):
            self.process_file()

        if not self.meta_info:
            return False
        torrent_pack = bool(re.search(r"S\d+(?!.*E\d+)", self.path))

        return  Contents(
            game_title=media.game_title,
            game_crew=media.crew,
            game_tags=media.game_tags,
            guess_title=media.guess_title,
            season=media.guess_season,
            episode=media.guess_episode,
            screen_size=media.screen_size,
            file_name=self.file_name,
            folder=self.folder,
            torrent_name=self.torrent_name,
            size=self.size,
            metainfo=self.meta_info,
            category=self.category,
            tracker_name=self.tracker_name,
            torrent_pack=torrent_pack,
            torrent_path=self.torrent_path,
            display_name=self.display_name,
            doc_description=self.doc_description,
            audio_languages=self.languages,
            game_nfo=self.game_nfo,
        )

    def process_file(self) -> bool:
        """Process individual files and gather metadata"""
        self.file_name = os.path.basename(self.path)
        # Get the current media folder
        self.folder = os.path.dirname(self.path)
        self.display_name, _ = os.path.splitext(self.file_name)
        self.display_name = ManageTitles.clean(self.display_name)
        self.torrent_path = self.path

        # Torrent name
        self.torrent_name = self.file_name

        # test to check if it is a doc
        self.doc_description = self.file_name
        self._handle_document_category()

        # Build meta_info
        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps([{"length": self.size, "path": [self.file_name]}], indent=4)
        return True

    def process_folder(self)-> bool:
        """Process folder and gather metadata for a torrent containing multiple files"""
        files_list = self.list_files_by_category()
        if not files_list:
            return False

        # Sample the first file in the list
        self.file_name = files_list[0]
        # Get the current media folder
        self.folder = self.path
        # Display name on webpage
        self.display_name = ManageTitles.clean(os.path.basename(self.path))
        # self._set_languages_from_title_or_media()

        self.torrent_path = self.path
        # Torrent name
        self.torrent_name = os.path.basename(self.path)
        # Document description
        self.doc_description = "\n".join(files_list)
        # test to check if it is a doc
        self._handle_document_category()

        # Build meta_info
        self.size = 0
        self.meta_info_list = []
        for file in files_list:
            size = os.path.getsize(os.path.join(self.path, file))
            self.meta_info_list.append({"length": size, "path": [file]})
            self.size += size
            if file.lower().endswith(".nfo"):
                self.game_nfo = os.path.join(self.path, file)

        self.meta_info = json.dumps(self.meta_info_list, indent=4)
        return True
    def list_files_by_category(self) -> list[str]:
        """List files based on the content category"""
        if self.category == self.tracker_data.category.get('game'):
            return self.list_game_files()
        return self.list_video_files()

    def list_video_files(self) -> list[str]:
        """List video files in the folder"""
        return [file for file in os.listdir(self.path) if ManageTitles.filter_ext(file)]

    def list_game_files(self) -> list[str]:
        """List all files in a game folder"""
        return [file for file in os.listdir(self.path)]

    def _handle_document_category(self)-> None:
        """Verify if it is a document"""
        media_docu_type = ManageTitles.media_docu_type(self.file_name)
        if media_docu_type:
            self.category = self.tracker_data.category.get(media_docu_type)