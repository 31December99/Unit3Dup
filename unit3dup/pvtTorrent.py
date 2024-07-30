# -*- coding: utf-8 -*-
import json
import os
import time
import torf
from tqdm import tqdm
from unit3dup.contents import Contents
from rich.console import Console

console = Console(log_path=False)


class HashProgressBar(tqdm):
    def callback(self, mytorr, path, current_num_hashed, total_pieces):
        progress_percentage = (current_num_hashed / total_pieces) * 100
        self.total = 100
        self.update(int(progress_percentage) - self.n)


class Mytorrent:

    def __init__(self, contents: Contents, meta: str):

        self.qb = None
        self.file_name = contents.file_name
        self.torrent_path = contents.torrent_path
        self.basename = os.path.basename(self.torrent_path)
        self.content_type = contents.category
        self.metainfo = json.loads(meta)

        self.mytorr = torf.Torrent(path=contents.torrent_path)
        self.mytorr.comment = "ciao"
        self.mytorr.name = contents.name
        self.mytorr.created_by = "Unit3d-Up"
        self.mytorr.private = True
        self.mytorr.segments = 16 * 1024 * 1024  # 16MB
        console.log(f"\n[ HASHING ] {self.mytorr.name}")
        start = time.time()
        with HashProgressBar() as progress:
            self.mytorr.generate(threads=4, callback=progress.callback, interval=0)
        end = time.time()
        console.log(f"Hashed in {end - start} s\n")

    def write(self) -> bool:
        try:
            self.mytorr.write(f"{self.torrent_path}.torrent")
            return True
        except torf.TorfError as e:
            console.log(e)
            return False

    @property
    def comment(self):
        return self.mytorr.comment

    @comment.setter
    def comment(self, value):
        self.mytorr.comment = value

    @property
    def info_hash(self):
        return self.mytorr.infohash
