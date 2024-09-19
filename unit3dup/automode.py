# -*- coding: utf-8 -*-

import os
from unit3dup.contents import Media
from common.utility.utility import Manage_titles
from common.utility import title
from common.trackers.trackers import ITTData
from common.custom_console import custom_console


class Auto:
    """
    A class for managing and processing video files and directories based on a given mode
    """

    def __init__(self, path: str, tracker_name=None, mode="auto"):  # todo: select the trackcer (tracker_name)
        """
        Initialize the Auto instance with path, tracker configuration, and mode.

        Args:
            path (str): The path to the directory or file to be processed.
            tracker_name (str): The name of the tracker configuration to be used.
            mode (str): The mode of operation, either 'auto', 'man', or 'folder'. Default is 'auto'.
        """
        tracker_data = ITTData.load_from_module()

        self.series = None
        self.movies = None
        self.path = path

        self.movie_category = tracker_data.category.get("movie")
        self.serie_category = tracker_data.category.get("tvshow")
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
                return self._lists(files_path=[], subfolders_path=series_path)

            if self.auto == "folder":
                # -f command (single folder series or 'saga')
                return self._lists(files_path=[], subfolders_path=[self.path])
        else:
            return self._lists(files_path=[self.path], subfolders_path=[])

    def scan(self):
        """
        Scans the directory for video files and subdirectories.

        If the path is a file, logs an error since scanning requires a folder. Otherwise, scans
        the folder and subfolders, sorting files and subdirectories, and processes them
        """
        files_path = []
        subfolders_path = []

        if not self.is_dir:
            custom_console.bot_error_log("We can't scan a file.")
        else:
            # Scan folder and subfolders
            for path, sub_dirs, files in os.walk(self.path):
                # Sort subdirs
                sub_dirs.sort(reverse=False)
                # Sort files
                files.sort(reverse=False)

                # Get the files path from the self.path
                if path == self.path:
                    files_path = [
                        os.path.join(self.path, file)
                        for file in files
                        if Manage_titles.filter_ext(file)
                    ]
                # Get the subfolders path from the self.path
                if sub_dirs:
                    # Maximum level of subfolder depth = 1
                    if self.depth_walker(path) < 1:
                        subfolders_path = [
                            os.path.join(self.path, subdir) for subdir in sub_dirs
                        ]
        return self._lists(files_path=files_path, subfolders_path=subfolders_path)

    def _lists(self, files_path: list, subfolders_path: list):

        return [
            result
            for media in files_path + subfolders_path
            if (result := self.create_media_path(media)) is not None
        ]

    def create_media_path(self, subdir: str) -> Media | None:

        file_name, ext = os.path.splitext(subdir)
        # wrong guessit with '-' char , example 'S01-'
        temp_name = Manage_titles.replace(subdir)
        guess_filename = title.Guessit(temp_name)

        if guess_filename.guessit_season:
            media_type = self.serie_category
        else:
            media_type = self.movie_category

        return Media(
            folder=self.path,
            subfolder=subdir,
            media_type=media_type,
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
