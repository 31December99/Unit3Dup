# -*- coding: utf-8 -*-

import os
import torf
from tqdm import tqdm

from unit3dup.tracker.data import trackers_api_data
from unit3dup.config.settings import Load
from unit3dup.view import custom_console
from unit3dup.media import Media

config_settings = Load().config


class HashProgressBar(tqdm):
    def callback(self, mytorr, path, current_num_hashed, total_pieces):
        if total_pieces:
            self.total = total_pieces
            self.update(current_num_hashed - self.n)


class Mytorrent:
    def __init__(self, contents: Media, tracker_name: str):
        self.tracker_name = tracker_name.upper()
        self.torrent_path = contents.torrent_path

        announce = trackers_api_data[self.tracker_name]['announce']

        self.mytorr = torf.Torrent(path=contents.torrent_path, trackers=announce)
        self.mytorr.comment = config_settings.user_preferences.TORRENT_COMMENT
        self.mytorr.name = contents.torrent_name
        self.mytorr.created_by = "https://github.com/31December99/Unit3Dup"
        self.mytorr.private = True
        self.mytorr.source = trackers_api_data[self.tracker_name]['source']
        self.mytorr.segments = 16 * 1024 * 1024

    def hash(self):
        # Calculate the torrent size
        size = round(self.mytorr.size / (1024 ** 3), 2)
        # Print a message for the user
        custom_console.print(f"\n'{self.tracker_name}' {self.mytorr.name} - {size} GB")
        # Hashing
        with HashProgressBar(
                desc="Hashing pieces",
                unit="piece",
                unit_scale=True,
                bar_format="{desc}: {bar} {n_fmt}/{total_fmt} pieces [{elapsed}<{remaining}, {rate_fmt}]",
                colour="#39FF14",
        ) as progress:
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
