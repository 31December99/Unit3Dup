# -*- coding: utf-8 -*-
import os
import time
import typing
import requests

from qbittorrent import Client
from common.config import config
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.contents import Contents
from common.custom_console import custom_console


class Qbitt:

    def __init__(
        self, tracker_data_response: str, torrent: Mytorrent, contents: Contents
    ):
        self.torrent = torrent
        self.torrent_path = contents.torrent_path
        self.torrent_file = None
        self.torrents = None
        self.torrent_archive = config.TORRENT_ARCHIVE

        self.qb = Client(f"{config.QBIT_URL}:{config.QBIT_PORT}/")
        download_torrent_dal_tracker = requests.get(tracker_data_response)

        if download_torrent_dal_tracker.status_code == 200:
            self.torrent_file = self.download(download_torrent_dal_tracker)
            self.qb.login(username=config.QBIT_USER, password=config.QBIT_PASS)
            self.qb.download_from_file(
                file_buffer=self.torrent_file, savepath=self.torrent.mytorr.location
            )
            time.sleep(3)
            # Get a torrent list
            self.torrents = self.qb.torrents()
            # Search for your torrent
            self.qbit(self.torrents)

    def download(self, link: requests) -> typing.IO:

        # Archive the torrent file if torrent_archive is set
        if self.torrent_archive:
            full_path_origin = f"{self.torrent_path}.torrent"
            file_name = f"{os.path.basename(self.torrent_path)}.torrent"
            full_path_archive = os.path.join(self.torrent_archive, file_name)
            os.replace(full_path_origin, full_path_archive)
        else:
            # Or save to current the path
            full_path_archive = f"{self.torrent_path}.torrent"

        # File archived
        with open(full_path_archive, "wb") as file:
            file.write(link.content)

        # Ready for seeding
        return open(full_path_archive, "rb")

    def qbit(self, torrents: list) -> bool:
        for torrent in torrents:
            if torrent["name"] == self.torrent.mytorr.name:
                infohash = torrent["hash"]
                # Location del torrent
                self.qb.recheck(infohash_list=infohash)
                custom_console.bot_log(f"\n[TORRENT INFOHASH]............  {infohash}")
                custom_console.bot_log(
                    f"[FILES LOCATION]..............  {self.torrent.mytorr.location}"
                )
                custom_console.bot_log(
                    f"[TORRENT NAME]................  {self.torrent.mytorr.name}.torrent"
                )
                return True
        custom_console.bot_error_log(
            f"I didn't find any torrents in the list matching yours {self.torrent.mytorr.name}"
        )
        return False
