# -*- coding: utf-8 -*-

import os
from rich.console import Console
from unit3dup.contents import File, Folder
from unit3dup.utility import Manage_titles
from unit3dup.command import config_tracker
from unit3dup import title

console = Console(log_path=False)


class Auto:

    def __init__(self, path: str, mode="auto"):
        self.series = None
        self.movies = None
        self.path = path
        self.movie_category = config_tracker.tracker_values.category("movie")
        self.serie_category = config_tracker.tracker_values.category("tvshow")
        self.is_dir = os.path.isdir(self.path)
        self.auto = mode

    def upload(self):

        if self.is_dir:
            series_path = [self.path]
            return self._lists(movies_path=[], series_path=series_path)
        else:
            movies_path = [self.path]
            return self._lists(movies_path=movies_path, series_path=[])

    def scan(self):
        movies_path = []
        series_path = []

        # when you use scan with file...
        # Path includes a filename. Os.walk requires a folder
        if not self.is_dir:
            console.log("Scan is only for folders..")
        else:
            for path, sub_dirs, files in os.walk(self.path):
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
        """Create a list of media object"""
        movies = [
            result
            for file in movies_path
            if (result := self.create_movies_path(file)) is not None
        ]

        # None in the series means a folder without a Sx tag
        # Walrus Operator
        series = [
            result
            for subdir in series_path
            if (result := self.create_folder_path(subdir)) is not None
        ]
        return series, movies

    def create_movies_path(self, file: str) -> File | None:
        """
        Determines if it is a movie or a series. Excludes any episode files.
        """
        file_name, ext = os.path.splitext(file)
        guess_filename = title.Guessit(file_name)
        if not guess_filename.guessit_season:
            # Movie without folder
            return File.create(
                file_name=file,
                folder=self.path,
                media_type=self.movie_category,
                torrent_name=guess_filename.guessit_title,
            )
        else:
            # Serie without folder
            return File.create(
                file_name=file,
                folder=self.path,
                media_type=self.serie_category,
                torrent_name=guess_filename.guessit_title,
            )

    def create_folder_path(self, subdir: str) -> Folder | None:
        """
        Determines whether the folder contains a Sx tag or it's a "movie folder"
        """
        file_name, ext = os.path.splitext(subdir)
        guess_filename = title.Guessit(file_name)
        if guess_filename.guessit_season:
            # Serie with folder
            return Folder.create(
                folder=self.path,
                subfolder=subdir,
                media_type=self.serie_category,
                torrent_name=guess_filename.guessit_title,
            )
        else:
            # Movie with folder
            return Folder.create(
                folder=self.path,
                subfolder=subdir,
                media_type=self.movie_category,
                torrent_name=guess_filename.guessit_title,
            )
            # return None  # Movie or generic file

    def depth_walker(self, path) -> int:
        """
        It stops at one subfolder and ignores any subfolders within that subfolder
        depth < 1
        """
        return path[len(self.path) :].count(os.sep)
