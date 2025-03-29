# -*- coding: utf-8 -*-
import argparse
import json
import os
import re

from common.utility import ManageTitles, System
from unit3dup.automode import Auto
from unit3dup.media import Media

class ContentManager:
    def __init__(self, path: str, mode: str, cli: argparse.Namespace):
        """
        Args:
            path (str): The path to the media files or directories
            mode (str):  mode 'manual' or 'automatic'
        """
        self.path = path
        self.mode = mode
        self.cli = cli

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
        self.tmdb_id: str | None = None
        self.imdb_id: str | None = None
        self.igdb_id: str | None = None
        self.generate_title: str | None = None

        self.path: str = os.path.normpath(path)
        self.auto = Auto(path=self.path, mode=self.mode)
        self.media_list = self.auto.upload() if self.mode in ["man", "folder"] else self.auto.scan()

    def process(self)-> list[Media]:
        contents = []
        for media in self.media_list:
            self.path = media.torrent_path
            media.category = media.category if not self.cli.force else self.cli.force
            self.category = media.category

            content = self.get_data(media=media)
            if content:
                contents.append(content)
        return contents

    def get_data(self, media: Media) -> Media | bool:
        """
        Process files or folders and create a `Contents` object if the metadata is valid
        """
        process = False
        if os.path.isdir(self.path):
            process = self.process_folder()
        elif os.path.isfile(self.path):
            process = self.process_file()

        if not self.meta_info:
            return False
        torrent_pack = bool(re.search(r"S\d+(?!.*E\d+)", self.path))

        if process:
            media.file_name = self.file_name
            media.torrent_name = self.torrent_name
            media.size = self.size
            media.metainfo = self.meta_info
            media.torrent_pack = torrent_pack
            media.doc_description = self.doc_description
            media.game_nfo = self.game_nfo
            media.display_name = self.display_name
            media.imdb_id = self.imdb_id
            media.tmdb_id = self.tmdb_id
            media.igdb_id = self.igdb_id
            return media
        else:
            return False

    def search_ids(self):
        _id = re.findall(r"\{(imdb-\d+|tmdb-\d+|igdb-\d+)}", self.file_name, re.IGNORECASE)
        if _id:
            # // Searching..
            for id in _id:
                if 'imdb-' in id:
                    self.imdb_id = id.replace('imdb-', '')
                    self.imdb_id = self.imdb_id if self.imdb_id.isdigit() else None
                elif 'tmdb-' in id:
                    self.tmdb_id = id.replace('tmdb-', '')
                    self.tmdb_id = self.tmdb_id if self.tmdb_id.isdigit() else None
                elif 'igdb-' in id:
                    self.igdb_id = id.replace('igdb-', '')
                    self.igdb_id = self.igdb_id if self.igdb_id.isdigit() else None
        else:
            self.imdb_id = None
            self.tmdb_id = None
            self.igdb_id = None

    def process_file(self) -> bool:
        """Process individual files and gather metadata"""
        self.file_name = self.path
        # Display name on webpage
        self.display_name, _ = os.path.splitext(os.path.basename(self.file_name))
        self.display_name = ManageTitles.clean(self.display_name)
        # current media path
        self.torrent_path = self.path
        # Try to get video ID from the string title
        self.search_ids()
        # Torrent name
        self.torrent_name =  os.path.basename(self.file_name)
        # test to check if it is a doc
        self.doc_description = self.file_name

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
        self.file_name = os.path.join(self.path, files_list[0])
        # Display name on webpage
        self.display_name = ManageTitles.clean(os.path.basename(self.path))
        # current media path
        self.torrent_path = self.path
        # Torrent name
        self.torrent_name = os.path.basename(self.path)
        # Document description
        self.doc_description = "\n".join(files_list)
        # Try to get video ID from the string title
        self.search_ids()
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
        if self.category ==System.category_list.get(System.GAME):
            return self.list_game_files()
        return self.list_video_files()

    def list_video_files(self) -> list[str]:
        """List video files in the folder"""
        return [file for file in os.listdir(self.path) if ManageTitles.filter_ext(file)]

    def list_game_files(self) -> list[str]:
        """List all files in a game folder"""
        return [file for file in os.listdir(self.path)]