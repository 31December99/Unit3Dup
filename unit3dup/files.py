# -*- coding: utf-8 -*-
import json
import os
import re

from unit3dup.contents import Contents
from common.trackers.trackers import ITTData
from common.utility.utility import Manage_titles
from common.mediainfo import MediaFile


class Files:
    """
    Identify the files (movies) and folders (series) regardless
    """

    def __init__(self, path: str, tracker_name: str, media_type: int, game_title: str, game_crew: list,
                 game_tags: list):
        self.languages = None
        self.display_name = None
        self.meta_info_list: list = []
        self.meta_info = None
        self.size = None
        self.name = None
        self.folder = None
        self.file_name = None
        self.torrent_path = None
        self.doc_description = None

        self.category: int = media_type
        self.game_title: str = game_title
        self.game_crew: list = game_crew
        self.game_tags: list = game_tags
        self.tracker_name: str = tracker_name
        self.path: str = path
        self.movies: list = []
        self.series: list = []
        self.is_dir = os.path.isdir(self.path)
        self.tracker_data = ITTData.load_from_module()

    def get_data(self) -> Contents | bool:
        """
        Create an object with movie or series attributes for the torrent.
        Verify if name is part of torrent pack folder
        """
        if not self.is_dir:
            # Check for valid extension
            process = (
                self.process_file() if Manage_titles.filter_ext(self.path) else False
            )
        else:
            process = self.process_folder()

        torrent_pack = bool(re.search(r"S\d+(?!.*E\d+)", self.path))
        return (
            Contents(
                file_name=self.file_name,
                folder=self.folder,
                name=self.name,
                size=self.size,
                metainfo=self.meta_info,
                category=self.category,
                tracker_name=self.tracker_name,
                torrent_pack=torrent_pack,
                torrent_path=self.torrent_path,
                display_name=self.display_name,
                doc_description=self.doc_description,
                audio_languages=self.languages,
                game_title=self.game_title,
                game_crew=self.game_crew,
                game_tags=self.game_tags,
            )
            if process
            else False
        )

    def process_file(self) -> bool:
        self.file_name = os.path.basename(self.path)
        self.folder = os.path.dirname(self.path)
        self.display_name, ext = os.path.splitext(self.file_name)
        self.display_name = Manage_titles.clean(self.display_name)
        self.torrent_path = os.path.join(self.folder, self.file_name)

        self.name = self.file_name
        self.doc_description = self.file_name
        media_info = MediaFile(file_path=os.path.join(self.folder, self.file_name))
        self.languages = media_info.available_languages
        media_docu_type = Manage_titles.media_docu_type(self.file_name)
        # If this is a document it becomes a document category
        if media_docu_type:
            # overwrite media_type # todo: 'cover image' not yet implemented
            self.category = self.tracker_data.category.get(media_docu_type)

        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps(
            [{"length": self.size, "path": [self.file_name]}], indent=4
        )
        return True

    def process_folder(self) -> bool:
        # Search for game files
        if self.game_crew:
            files = self.list_game_files()
        else:
            # Search for video files
            files = self.list_video_files()

        if not files:
            return False

        self.meta_info_list = []
        self.file_name = files[0]
        self.folder = self.path
        self.display_name = Manage_titles.clean(os.path.basename(self.path))
        self.torrent_path = self.folder
        self.name = os.path.basename(self.folder)
        self.doc_description = "\n".join(files)
        media_info = MediaFile(file_path=os.path.join(self.folder, self.file_name))
        self.languages = media_info.available_languages

        media_docu_type = Manage_titles.media_docu_type(self.file_name)
        # If there is a document in the folder it becomes a document folder
        if media_docu_type:
            # overwrite media_type # todo: 'cover image' not yet implemented
            self.category = self.tracker_data.category.get(media_docu_type)

        total_size = 0
        for file in files:
            size = os.path.getsize(os.path.join(self.folder, file))
            self.meta_info_list.append({"length": size, "path": [file]})
            total_size += size
        self.size = total_size
        self.meta_info = json.dumps(self.meta_info_list, indent=4)
        return True

    def list_video_files(self) -> list:
        """
        Add every video file to the list
        """
        return [
            file for file in os.listdir(self.path) if Manage_titles.filter_ext(file)
        ]

    def list_game_files(self) -> list:
        """
        Add every file to the list
        """
        return [
            file for file in os.listdir(self.path)
        ]
