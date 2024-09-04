# -*- coding: utf-8 -*-

import os
from unit3dup.contents import File, Folder
from common.utility.utility import Manage_titles
from common.utility import title
from common.config import config
from common.custom_console import custom_console


class Auto:
    """
    A class for managing and processing video files and directories based on a given mode
    """

    def __init__(self, path: str, tracker_name: str, mode="auto"):
        """
        Initialize the Auto instance with path, tracker configuration, and mode.

        Args:
            path (str): The path to the directory or file to be processed.
            tracker_name (str): The name of the tracker configuration to be used.
            mode (str): The mode of operation, either 'auto', 'man', or 'folder'. Default is 'auto'.
        """
        self.series = None
        self.movies = None
        self.path = path
        self.config = config.trackers.get_tracker(tracker_name)
        self.movie_category = self.config.tracker_values.category("movie")
        self.serie_category = self.config.tracker_values.category("tvshow")
        self.is_dir = os.path.isdir(self.path)
        self.auto = mode

    def upload(self):
        """
        Handles the upload process based on the specified mode.

        If the path is a directory, it processes video files and directories according to the mode:
        - 'man': Single file or scan each file in the folder
        - 'folder': Single folder series or 'saga'
        If the path is not a directory, it processes the path as a single file
        """
        if self.is_dir:
            series_path = self.list_video_files(self.path)

            if self.auto == "man":
                # -u command (single file or scan each file in the folder)
                return self._lists(movies_path=[], series_path=series_path)

            if self.auto == "folder":
                # -f command (single folder series or 'saga')
                return self._lists(movies_path=[], series_path=[self.path])
        else:
            return self._lists(movies_path=[self.path], series_path=[])

    def scan(self):
        """
        Scans the directory for video files and subdirectories.

        If the path is a file, logs an error since scanning requires a folder. Otherwise, scans
        the folder and subfolders, sorting files and subdirectories, and processes them.
        """
        movies_path = []
        series_path = []

        if not self.is_dir:
            custom_console.bot_error_log("We can't scan a file.")
        else:
            # Scan folder and subfolders
            for path, sub_dirs, files in os.walk(self.path):
                # Sort subdirs
                sub_dirs.sort(reverse=False)
                # Sort files
                files.sort(reverse=False)

                if path == self.path:
                    movies_path = [
                        os.path.join(self.path, file)
                        for file in files
                        if Manage_titles.filter_ext(file)
                    ]
                if sub_dirs:
                    # Maximum level of subfolder depth = 1
                    if self.depth_walker(path) < 1:
                        series_path = [
                            os.path.join(self.path, subdir) for subdir in sub_dirs
                        ]
        return self._lists(movies_path=movies_path, series_path=series_path)

    def _lists(self, movies_path: list, series_path: list):
        """
        Creates a list of media objects from given movie and series paths.

        Args:
            movies_path (list): A list of paths to movie files.
            series_path (list): A list of paths to series directories.

        Returns:
            list: A combined list of File and Folder objects created from the paths.
        """
        movies = [
            result
            for file in movies_path
            if (result := self.create_file_path(file)) is not None
        ]

        # None in the series means a folder without a Sx tag
        series = [
            result
            for subdir in series_path
            if (result := self.create_folder_path(subdir)) is not None
        ]
        return series + movies

    def create_file_path(self, file: str) -> File | None:
        """
        Creates a File object from a given file path.

        Args:
            file (str): The path to the file.

        Returns:
            File | None: A File object created from the path, or None if not applicable.
        """
        file_name, ext = os.path.splitext(file)
        guess_filename = title.Guessit(file_name)
        if guess_filename.guessit_season:
            media_type = self.serie_category
        else:
            media_type = self.movie_category

        return File.create(
            file_name=file,
            folder=self.path,
            media_type=media_type,
            torrent_name=guess_filename.guessit_title,
            source=guess_filename.source,
            other=guess_filename.other,
            audio_codec=guess_filename.audio_codec,
            subtitle=guess_filename.subtitle,
            resolution=guess_filename.screen_size,
        )

    def create_folder_path(self, subdir: str) -> Folder | None:
        """
        Determines whether the folder contains a season tag or is a "movie folder" and creates a Folder object.

        Args:
            subdir (str): The name of the subdirectory.

        Returns:
            Folder | None: A Folder object created from the subdirectory, or None if not applicable.
        """
        file_name, ext = os.path.splitext(subdir)
        guess_filename = title.Guessit(file_name)

        if guess_filename.guessit_season:
            media_type = self.serie_category
        else:
            media_type = self.movie_category

        return Folder.create(
            folder=self.path,
            subfolder=subdir,
            media_type=media_type,
            torrent_name=guess_filename.guessit_title,
            source=guess_filename.source,
            other=guess_filename.other,
            audio_codec=guess_filename.audio_codec,
            subtitle=guess_filename.subtitle,
            resolution=guess_filename.screen_size,
        )

    def depth_walker(self, path) -> int:
        """
        Calculates the depth of a given path relative to the base path.

        Args:
            path (str): The path to evaluate.

        Returns:
            int: The depth level of the path, where depth < 1 indicates a maximum of one level of subfolders
        """
        return path[len(self.path) :].count(os.sep)

    @staticmethod
    def list_video_files(manual_path: str) -> list:
        """
        Lists all video files in a given directory based on their extension

        Args:
            manual_path (str): The directory path to scan for video files

        Returns:
            list: A list of video files in the directory that match the video file extensions
        """
        return [
            file for file in os.listdir(manual_path) if Manage_titles.filter_ext(file)
        ]
