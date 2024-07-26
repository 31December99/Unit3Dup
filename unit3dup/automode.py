# -*- coding: utf-8 -*-

import os
from rich.console import Console
from unit3dup.contents import File, Folder
from unit3dup.utility import Manage_titles
from unit3dup import title

console = Console(log_path=False)


class Auto:

    def __init__(self, path: str):
        self.series = None
        self.movies = None
        self.path = path

    def scan(self):
        movies_path = []
        series_path = []

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

        self.movies = [
            self.create_movies_path(file)
            for file in movies_path
            if self.create_movies_path(file) is not None
        ]
        # None in the series means a folder without an Sx tag
        self.series = [self.create_series_path(subdir) for subdir in series_path]
        return self.series, self.movies

    def create_movies_path(self, file: str) -> File | None:
        """
        Determines if it is a movie or a series. Excludes any episode files.
        """
        file_name, ext = os.path.splitext(file)
        guess_filename = title.Guessit(file_name)
        if not guess_filename.guessit_season:
            return File.create(file_name=file, folder=self.path, media_type="1")
        else:
            return None

    def create_series_path(self, subdir: str) -> Folder | None:
        """
        Determines whether the folder contains an Sx tag
        """
        file_name, ext = os.path.splitext(subdir)
        guess_filename = title.Guessit(file_name)
        if guess_filename.guessit_season:
            return Folder.create(folder=self.path, subfolder=subdir, media_type="2")
        else:
            return None

    def depth_walker(self, path) -> int:
        """
        It stops at one subfolder and ignores any subfolders within that subfolder
        depth < 1
        """
        return path[len(self.path):].count(os.sep)
