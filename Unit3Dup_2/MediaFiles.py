# -*- coding: utf-8 -*-

import json
import os
import re

from rich.console import Console

console = Console(log_path=False)


class Contents:

    def __init__(self, file_name: str, folder: str, name: str, size: int, metainfo: json, category: int,
                 tracker_name: str, torrent_pack: bool):
        self.file_name = file_name
        self.name = name
        self.folder = folder
        self.size = size
        self.metainfo = metainfo
        self.category = category
        self.tracker_name = tracker_name
        self.torrent_pack = torrent_pack

    @classmethod
    def create_instance(cls, file_name: str, folder: str, name: str, size: int, metainfo: json, category: int,
                        tracker_name: str, torrent_pack: bool):
        return cls(file_name, folder, name, size, metainfo, category, tracker_name, torrent_pack)


class MediaFiles:

    def __init__(self, path: str, tracker: str = 'itt'):
        self.path = path
        self.tracker = tracker
        self.is_dir = os.path.isdir(self.path)
        self.meta_info_list = None
        self.meta_info = None
        self.size = None
        self.name = None
        self.category = None
        self.folder = None
        self.file_name = None

    def process_file(self) -> bool:
        self.file_name = os.path.basename(self.path)
        self.folder = os.path.dirname(self.path)
        self.category = 1
        self.name, ext = os.path.splitext(self.file_name)
        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps([{'length': self.size, 'path': [self.file_name]}], indent=4)
        return True

    def process_folder(self) -> bool:
        files = self.list_video_files()

        if not files:
            console.log(f"\n*** '{self.path}' No video files found in the directory - skip ***\n")
            return False

        self.file_name = files[0]
        self.folder = self.path
        self.category = 2
        self.name, ext = os.path.splitext(self.file_name)

        self.meta_info_list = []
        total_size = 0
        for file in files:
            size = os.path.getsize(os.path.join(self.folder, file))
            self.meta_info_list.append({'length': size, 'path': [file]})
            total_size += size
        self.size = total_size
        self.meta_info = json.dumps(self.meta_info_list, indent=4)
        return True

    def depth_walker(self, path) -> int:
        """
            It stops at one subfolder and ignores any subfolders within that subfolder
            depth < 1
        """
        return path[len(self.path):].count(os.sep)

    def filter_ext(self, file: str) -> bool:

        video_ext = [
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".3gp", ".ogg",
            ".mpg", ".mpeg", ".m4v", ".rm", ".rmvb", ".vob", ".ts", ".m2ts", ".divx",
            ".asf", ".swf", ".ogv", ".drc", ".m3u8"
        ]

        return os.path.splitext(file)[1].lower() in video_ext

    def list_video_files(self) -> list:
        """
        Add to the list every file if its extension is in the video_ext.
        """
        print("list video files")
        print(os.listdir)

        return [file for file in os.listdir(self.path) if self.filter_ext(file)]

    def get_data(self) -> Contents | bool:
        pass


class Files(MediaFiles):

    def __init__(self, path: str, tracker: str = 'itt'):
        super().__init__(path, tracker)
        self.path = path
        self.tracker = tracker
        self.is_dir = os.path.isdir(self.path)
        self.meta_info_list = None
        self.meta_info = None
        self.size = None
        self.name = None
        self.category = None
        self.folder = None
        self.file_name = None

    def get_data(self) -> Contents | bool:
        # Check for valid extension
        process = self.process_file() if self.filter_ext(self.path) else False

        return Contents.create_instance(
            file_name=self.file_name,
            folder=self.folder,
            name=self.name,
            size=self.size,
            metainfo=self.meta_info,
            category=self.category,
            tracker_name=self.tracker,
            torrent_pack=False
        ) if process else False


class Folders(MediaFiles):

    def __init__(self, path: str, tracker: str = 'itt'):
        super().__init__(path, tracker)
        self.path = path
        self.tracker = tracker
        self.is_dir = os.path.isdir(self.path)
        self.meta_info_list = None
        self.meta_info = None
        self.size = None
        self.name = None
        self.category = None
        self.folder = None
        self.file_name = None

    def get_data(self) -> Contents | bool:
        # Check for valid extension
        process = self.process_folder() if self.filter_ext(self.path) else False
        print("P", process)

        torrent_pack = bool(re.search(r'S\d+(?!.*E\d+)', self.path))
        console.log(f"\n[TORRENT PACK] {torrent_pack}...  '{self.path}'")

        return Contents.create_instance(
            file_name=self.file_name,
            folder=self.folder,
            name=self.name,
            size=self.size,
            metainfo=self.meta_info,
            category=self.category,
            tracker_name=self.tracker,
            torrent_pack=False
        ) if process else False
