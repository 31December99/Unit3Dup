import json
import os
from typing import Union
from unit3dup import userinput, title
from rich.console import Console

console = Console(log_path=False)


class File:
    """
    For each File , create an object with attributes:
    file_name, folder, media_type
    """

    def __init__(self, file_name: str, folder: str, media_type: str):
        self.file_name = os.path.join(folder, file_name)
        self.folder = folder
        self.media_type = media_type

    @classmethod
    def create(cls, file_name: str, folder: str, media_type: str):
        return cls(file_name, folder, media_type)


class Folder:
    """
    For each Folder, create an object with attributes:
    folder, subfolder, media_type
    """

    def __init__(self, folder: str, subfolder: str, media_type: str):
        self.folder = os.path.join(folder, subfolder)
        self.subfolder = subfolder
        self.media_type = media_type

    @classmethod
    def create(cls, folder: str, subfolder: str, media_type: str):
        return cls(folder, subfolder, media_type)


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

    def get_data(self) -> [userinput.Contents, bool]:
        """
        Create an userinput object with movie or series attributes for the torrent.
        """
        if not self.is_dir:
            # Check for valid extension
            process = self.process_file() if self.filter_ext(self.path) else False
        else:
            process = self.process_folder()

        return userinput.Contents(
            file_name=self.file_name,
            folder=self.folder,
            name=self.name,
            size=self.size,
            metainfo=self.meta_info,
            category=self.category,
            tracker_name=self.tracker
        ) if process else False

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

    def search_files(self, file: str) -> Union[File, None]:
        """
        Determines if it is a movie or a series. Excludes any episode files.
        """
        file_name, ext = os.path.splitext(file)
        guess_filename = title.Guessit(file_name)
        if not guess_filename.guessit_season:
            return File.create(file_name=file, folder=self.path, media_type='1')
        else:
            return None

    def search_folder(self, subdir: str) -> Union[Folder, None]:
        return Folder.create(folder=self.path, subfolder=subdir, media_type='2')

    def start(self) -> [list, list]:
        """
        If the provided path does not represent a directory, return an empty list.
        Create a list of File objects for each movie present.
        """
        if not self.is_dir:
            console.log("Wrong Path!")
            return []

        return self.walker()

    def filter_ext(self, file: str) -> bool:

        video_ext = [
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".3gp", ".ogg",
            ".mpg", ".mpeg", ".m4v", ".rm", ".rmvb", ".vob", ".ts", ".m2ts", ".divx",
            ".asf", ".swf", ".ogv", ".drc", ".m3u8"
        ]

        return os.path.splitext(file)[1].lower() in video_ext

    def walker(self) -> [list, list]:
        """
         Analyze the path and create a list for movies and a list for series.
         All files without the SxEx tag inside the path are considered movies.
         Each folder inside the path is considered a series.
        """

        movies_path = []
        series_path = []
        for path, subdirs, files in os.walk(self.path):
            if path == self.path:
                movies_path = [os.path.join(self.path, file) for file in files if self.filter_ext(file)]
            if subdirs:
                if self.depth_walker(path) < 1:
                    series_path = [os.path.join(self.path, subdir) for subdir in subdirs]

        movies = [self.search_files(file) for file in movies_path if self.search_files(file) is not None]
        series = [self.search_folder(subdir) for subdir in series_path]

        if not movies and not series:
            console.log(f"[Walker says there's nothing here..] '{self.path}'")
            console.log("Remember, within the folder of your path, there must be files (movies) or folders (series)."
                        " Files representing episodes without folders will not be considered")
        return movies, series

    def depth_walker(self, path) -> int:
        """
            It stops at one subfolder and ignores any subfolders within that subfolder
            depth < 1
        """
        return path[len(self.path):].count(os.sep)

    def list_video_files(self) -> list:
        """
        Add to the list every file if its extension is in the video_ext.
        """

        return [file for file in os.listdir(self.path) if self.filter_ext(file)]
