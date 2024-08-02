# -*- coding: utf-8 -*-
import time
import typing
import requests

from rich.console import Console
from qbittorrent import Client
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.contents import Contents
from unit3dup import config

console = Console(log_path=False)


class Qbitt:

    def __init__(
        self, tracker_data_response: str, torrent: Mytorrent, contents: Contents
    ):
        self.torrent = torrent
        self.torrent_path = contents.torrent_path
        self.torrent_file = None
        self.torrents = None

        # c'e ancora da fare service
        self.qb = Client(f"{config.QBIT_URL}:{config.QBIT_PORT}/")
        download_torrent_dal_tracker = requests.get(tracker_data_response)

        if download_torrent_dal_tracker.status_code == 200:
            self.torrent_file = self.download(download_torrent_dal_tracker)
            self.qb.login(username=config.QBIT_USER, password=config.QBIT_PASS)
            self.qb.download_from_file(
                file_buffer=self.torrent_file, savepath=self.torrent.mytorr.location
            )
            time.sleep(3)
            # Ottieni la lista dei torrent
            self.torrents = self.qb.torrents()
            # Trova il torrent desiderato
            self.qbit(self.torrents)

    def download(self, link: requests) -> typing.IO:
        with open(f"{self.torrent_path}.torrent", "wb") as file:
            file.write(link.content)
        return open(f"{self.torrent_path}.torrent", "rb")

    def qbit(self, torrents: list) -> bool:
        for torrent in torrents:
            if torrent["name"] == self.torrent.mytorr.name:
                infohash = torrent["hash"]
                # Location del torrent
                self.qb.recheck(infohash_list=infohash)
                console.log(f"\n[TORRENT INFOHASH]............  {infohash}")
                console.log(
                    f"[TORRENT LOCATION]............  {self.torrent.mytorr.location}"
                )
                console.log(
                    f"[TORRENT NAME]................  {self.torrent.mytorr.name}.torrent"
                )
                return True
        console.log(
            f"Non ho trovato nessun torrents in list corrispondente al tuo {self.torrent.mytorr.name}"
        )
        return False
