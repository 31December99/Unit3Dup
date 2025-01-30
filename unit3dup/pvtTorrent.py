# -*- coding: utf-8 -*-

import json
import os
import torf
from tqdm import tqdm
from common.custom_console import custom_console
from unit3dup import config
from unit3dup.contents import Contents


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
        self.mytorr.comment = config.TORRENT_COMMENT
        self.mytorr.name = contents.name
        self.mytorr.created_by = "https://github.com/31December99/Unit3Dup"
        self.mytorr.private = True
        self.mytorr.segments = 16 * 1024 * 1024

    def hash(self):
        custom_console.print(f"\n[ HASHING ] {self.mytorr.name}")
        with HashProgressBar() as progress:
            try:
                self.mytorr.generate(threads=4, callback=progress.callback, interval=0)
            except torf.TorfError as e:
                custom_console.bot_error_log(e)
                exit(1)

    def write(self) -> bool:
        if not config.TORRENT_ARCHIVE:
            full_path = f"{self.torrent_path}.torrent"
        else:
            torrent_file_name = os.path.basename(self.torrent_path)
            full_path = os.path.join(
                config.TORRENT_ARCHIVE, f"{torrent_file_name}.torrent"
            )

        custom_console.bot_log(f"--> {full_path}")

        try:
            self.mytorr.write(full_path)
            return True
        except torf.TorfError as e:
            if "File exists" in str(e):
                custom_console.bot_error_log(
                    f"This torrent file already exists: {full_path}"
                )
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
