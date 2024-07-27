# -*- coding: utf-8 -*-
import json
import os
import re
from rich.console import Console

from unit3dup.contents import Contents
from unit3dup.utility import Manage_titles
from unit3dup.command import config_tracker

console = Console(log_path=False)


class Files:
    """
    e identificare quelli che sono i files(movies) e i folder(series)

    """

    def __init__(self, path: str, tracker: str):
        self.meta_info_list: list = []
        self.meta_info = None
        self.size = None
        self.name = None
        self.category = None
        self.folder = None
        self.file_name = None
        self.tracker: str = tracker
        self.path: str = path
        self.movies: list = []
        self.series: list = []
        self.is_dir = os.path.isdir(self.path)

    def get_data(self) -> Contents | bool:
        """
        Create an userinput object with movie or series attributes for the torrent.
        Verify if name is part of torrent pack folder. If there is no episode it's a pack
        """
        if not self.is_dir:
            # Check for valid extension
            process = (
                self.process_file() if Manage_titles.filter_ext(self.path) else False
            )
        else:
            process = self.process_folder()

        torrent_pack = bool(re.search(r"S\d+(?!.*E\d+)", self.path))
        console.log(f"\n[TORRENT PACK] {torrent_pack}...  '{self.path}'")

        return (
            Contents.create_instance(
                file_name=self.file_name,
                folder=self.folder,
                name=self.name if not self.is_dir else os.path.basename(self.folder),
                size=self.size,
                metainfo=self.meta_info,
                category=self.category,
                tracker_name=self.tracker,
                torrent_pack=torrent_pack,
            )
            if process
            else False
        )

    def process_file(self) -> bool:
        self.file_name = os.path.basename(self.path)
        self.folder = os.path.dirname(self.path)
        self.category = config_tracker.tracker_values.category('movie')
        self.name, ext = os.path.splitext(self.file_name)
        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps(
            [{"length": self.size, "path": [self.file_name]}], indent=4
        )
        return True

    def process_folder(self) -> bool:
        files = self.list_video_files()
        if not files:
            console.log(
                f"\n*** '{self.path}' No video files found in the directory - skip ***\n"
            )
            return False

        self.file_name = files[0]
        self.folder = self.path
        self.category = config_tracker.tracker_values.category('tvshow')
        self.name, ext = os.path.splitext(self.file_name)

        self.meta_info_list = []
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
        Add to the list every file if its extension is in the video_ext.
        """
        return [
            file for file in os.listdir(self.path) if Manage_titles.filter_ext(file)
        ]
