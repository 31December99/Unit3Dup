#!/usr/bin/env python3.9
import os
from pathlib import Path, PurePath
from decouple import config
import torf

import utitlity

ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')


class Mytorrent:

    def __init__(self, contents: str):
        self.contents = Path(contents)
        self.file_name = PurePath(self.contents).name if Path.is_dir(self.contents) else Path(contents).name
        self.title, self.extension = os.path.splitext(self.file_name)
        self.mytorr = torf.Torrent(path=self.file_name)
        self.mytorr.announce_list = [f"https://itatorrents.xyz/announce/{ITT_PASS_KEY}/"]
        self.mytorr.comment = "ciao"
        self.mytorr.name = self.file_name
        self.mytorr.generate()
        self.mytorr.created_by = "bITT"
        self.mytorr.private = True
        self.mytorr.segments = 16 * 1024 * 1024  # 16MB

    def write(self):
        self.mytorr.write(f"{self.file_name}.torrent")

    @property
    def comment(self):
        return self.mytorr.comment

    @comment.setter
    def comment(self, value):
        self.mytorr.comment = value

    @property
    def name(self):
        return self.title

    @property
    def info_hash(self):
        return self.mytorr.infohash
