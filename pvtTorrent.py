#!/usr/bin/env python3.9
from pathlib import Path, PurePath
import torf


class Mytorrent:

    def __init__(self, contents: str):
        self.contents = Path(contents)
        self.file_name = PurePath(self.contents).name if Path.is_dir(self.contents) else Path(contents).name
        self.mytorr = torf.Torrent(path=self.file_name)
        self.mytorr.generate()
        self.mytorr.created_by = "bITT"
        self.mytorr.private = True
        self.mytorr.segments = 16 * 1024 * 1024  # 16MB

    def write(self, torrent_filename: str):
        self.mytorr.write(f"{torrent_filename}.torrent")

    @property
    def comment(self):
        return self.mytorr.comment

    @comment.setter
    def comment(self, value):
        self.mytorr.comment = value

    @property
    def name(self):
        return self.mytorr.name

    @name.setter
    def name(self, value):
        self.mytorr.name = value

    @property
    def info_hash(self):
        return self.mytorr.infohash
