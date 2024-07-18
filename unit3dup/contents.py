import json
import os
from typing import Union
from unit3dup import userinput, title


class File:
    def __init__(self, file_name: str, folder: str, media_type: str):
        self.file_name = os.path.join(folder, file_name)
        self.folder = folder
        self.media_type = media_type

    @classmethod
    def create(cls, file_name: str, folder: str, media_type: str):
        return cls(file_name, folder, media_type)


class Cli:
    """
    A class to recognize series from movies and return an object with attributes:

    Attributes:
        file_name: The name of the torrent file.
        folder: The name of the folder containing the file.
        name: The name of the torrent.
        size: The size of the movie or series.
        meta_info: A dictionary containing metadata of the files for the torrent.
        category: A value that reflects the tracker's database, corresponding to movie or series.

    TODO:
        Remove the hardcoded category value and read it from a JSON configuration file.
    """

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

    def what_media_type(self, file: str) -> Union[File, None]:
        """
        Determines if it is a movie or a series. Excludes any episode files.
        """
        file_name, ext = os.path.splitext(file)
        guess_filename = title.Guessit(file_name)

        if not guess_filename.guessit_season:
            return File.create(file_name=file, folder=self.path, media_type='1')
        return None

    def start(self) -> list:
        """
        If the provided path does not represent a directory, return an empty list.
        Create a list of File objects for each movie present.
        """
        if not self.is_dir:
            return []

        files = self.list_video_files()
        return [self.what_media_type(file) for file in files if self.what_media_type(file) is not None]

    def get_data(self) -> userinput.Contents:
        """
        Create a userinput object with movie or series attributes for the torrent.
        """
        if not self.is_dir:
            self.process_file()
        else:
            self.process_folder()

        return userinput.Contents(
            file_name=self.file_name,
            folder=self.folder,
            name=self.name,
            size=self.size,
            metainfo=self.meta_info,
            category=self.category,
            tracker_name=self.tracker
        )

    def process_file(self):
        self.file_name = os.path.basename(self.path)
        self.folder = os.path.dirname(self.path)
        self.category = 1
        self.name, ext = os.path.splitext(self.file_name)
        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps([{'length': self.size, 'path': [self.file_name]}], indent=4)

    def process_folder(self):
        files = self.list_video_files()
        if not files:
            raise ValueError("No video files found in the directory.")

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

    def list_video_files(self) -> list:
        """
        Add to the list every file if its extension is in the video_ext.
        """
        video_ext = [
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".3gp", ".ogg",
            ".mpg", ".mpeg", ".m4v", ".rm", ".rmvb", ".vob", ".ts", ".m2ts", ".divx",
            ".asf", ".swf", ".ogv", ".drc", ".m3u8"
        ]
        return [file for file in os.listdir(self.path) if os.path.splitext(file)[1].lower() in video_ext]
