# -*- coding: utf-8 -*-
import json
import os
import time
import sys
import torf
from decouple import Config, RepositoryEnv
from tqdm import tqdm
from unit3dup.contents import Contents
from rich.console import Console


config_load = Config(RepositoryEnv('service.env'))
console = Console(log_path=False)

QBIT_USER = config_load('QBIT_USER')
QBIT_PASS = config_load('QBIT_PASS')
QBIT_URL = config_load('QBIT_URL')
QBIT_PORT = config_load('QBIT_PORT')


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
        print(f"[Mytorrent] torrent path {self.torrent_path}")

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

    def write(self):
        try:
            self.mytorr.write(f"{self.torrent_path}.torrent")
        except torf.TorfError as e:
            print(e)
            sys.exit()
        return self.mytorr


    @property
    def comment(self):
        return self.mytorr.comment

    @comment.setter
    def comment(self, value):
        self.mytorr.comment = value

    @property
    def info_hash(self):
        return self.mytorr.infohash
