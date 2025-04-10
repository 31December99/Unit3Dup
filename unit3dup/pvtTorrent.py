# -*- coding: utf-8 -*-

import json
import os
import torf
from tqdm import tqdm

from common.trackers.data import trackers_api_data
from unit3dup.media import Media
from unit3dup import config_settings

from view import custom_console

class HashProgressBar(tqdm):
    def callback(self, mytorr, path, current_num_hashed, total_pieces):
        progress_percentage = (current_num_hashed / total_pieces) * 100
        self.total = 100
        self.update(int(progress_percentage) - self.n)

class Mytorrent:

    def __init__(self, contents: Media, meta: str, trackers_list = None):

        self.torrent_path = contents.torrent_path
        self.trackers_list = trackers_list

        announces = []
        # one tracker at time
        for tracker_name in trackers_list:
            announce = trackers_api_data[tracker_name.upper()]['announce'] if tracker_name else None
            announces.append([announce])

        self.metainfo = json.loads(meta)
        self.mytorr = torf.Torrent(path=contents.torrent_path, trackers=announces)
        self.mytorr.comment = config_settings.user_preferences.TORRENT_COMMENT
        self.mytorr.name = contents.torrent_name
        self.mytorr.created_by = "https://github.com/31December99/Unit3Dup"
        self.mytorr.private = True
        self.mytorr.source= trackers_api_data[trackers_list[0]]['source']
        self.mytorr.segments = 16 * 1024 * 1024


    def hash(self):
        custom_console.print(f"\n{self.trackers_list} {self.mytorr.name}")
        with HashProgressBar() as progress:
            try:
                self.mytorr.generate(threads=4, callback=progress.callback, interval=0)
            except torf.TorfError as e:
                custom_console.bot_error_log(e)
                exit(1)

    def write(self, overwrite: bool, full_path: str) -> bool:
        try:
            if overwrite:
                os.remove(full_path)
            self.mytorr.write(full_path)
            return True
        except torf.TorfError as e:
            if "File exists" in str(e):
                custom_console.bot_error_log(f"This torrent file already exists: {full_path}")
            return False
        except FileNotFoundError as e:
            custom_console.bot_error_log(f"Trying to update torrent but it does not exist: {full_path}")
            return False
