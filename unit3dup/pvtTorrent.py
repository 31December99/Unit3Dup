# -*- coding: utf-8 -*-

import json
import os
import torf
from tqdm import tqdm

from unit3dup.media import Media
from unit3dup import config_settings

from view import custom_console

class HashProgressBar(tqdm):
    def callback(self, mytorr, path, current_num_hashed, total_pieces):
        progress_percentage = (current_num_hashed / total_pieces) * 100
        self.total = 100
        self.update(int(progress_percentage) - self.n)


class Mytorrent:

    def __init__(self, contents: Media, meta: str):

        # If shared_path is None set the path to the value of torrent_path
        if not config_settings.torrent_client_config.SHARED_PATH:
            # shared path
            self.torrent_path = contents.torrent_path
        else:
            # local path
            self.torrent_path = config_settings.torrent_client_config.SHARED_PATH

        # Check if torrent_path exist
        if not os.path.exists(self.torrent_path):
            custom_console.bot_error_log(f"Torrent path '{self.torrent_path}' does not exist")
            custom_console.bot_error_log(f"Please check your path and retry")
            exit(1)

        self.metainfo = json.loads(meta)
        self.mytorr = torf.Torrent(path=contents.torrent_path)
        self.mytorr.comment = config_settings.user_preferences.TORRENT_COMMENT
        self.mytorr.name = contents.torrent_name
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
        if not config_settings.user_preferences.TORRENT_ARCHIVE:
            full_path = f"{self.torrent_path}.torrent"
        else:
            torrent_file_name = os.path.basename(self.torrent_path)
            full_path = os.path.join(
                config_settings.user_preferences.TORRENT_ARCHIVE, f"{torrent_file_name}.torrent"
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