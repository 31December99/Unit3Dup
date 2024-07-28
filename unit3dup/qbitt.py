# -*- coding: utf-8 -*-
import time
import typing
from urllib.parse import urljoin

import requests
from rich.console import Console
from qbittorrent import Client
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.contents import Contents
from unit3dup.command import config_tracker

console = Console(log_path=False)


class Qbitt:

    def __init__(self, tracker_data_response: str, torrent: Mytorrent, contents: Contents):

        self.qbit_user = config_tracker.instance.qbit_user
        self.qbit_pass = config_tracker.instance.qbit_pass
        self.qbit_url = config_tracker.instance.qbit_url
        self.qbit_port = config_tracker.instance.qbit_port
        self.torrent = torrent
        self.torrent_path = contents.torrent_path
        self.torrent_file = None
        self.torrents = None

        self.qb = Client(f'{self.qbit_url}:{self.qbit_port}/')
        # self.qb = urljoin(self.qbit_url, self.qbit_port)

        download_torrent_dal_tracker = requests.get(tracker_data_response)

        if download_torrent_dal_tracker.status_code == 200:
            self.torrent_file = self.download(download_torrent_dal_tracker)
            self.qb.login(username=self.qbit_user, password=self.qbit_pass)
            self.qb.download_from_file(file_buffer=self.torrent_file, savepath=self.torrent.mytorr.location)
            time.sleep(3)
            # Ottieni la lista dei torrent
            self.torrents = self.qb.torrents()
            print(self.torrents)
            # Trova il torrent desiderato
            self.qbit(self.torrents)

    def download(self, link: requests) -> typing.IO:
        with open(f'{self.torrent_path}.torrent', 'wb') as file:
            file.write(link.content)
        return open(f'{self.torrent_path}.torrent', 'rb')

    def qbit(self, torrents: list) -> bool:
        for torrent in torrents:
            print(self.torrent.mytorr.name)

            if torrent['name'] == self.torrent.mytorr.name:
                infohash = torrent['hash']
                # Location del torrent
                self.qb.recheck(infohash_list=infohash)
                console.log(f'\n[TORRENT INFOHASH]............  {infohash}')
                console.log(f'[TORRENT LOCATION]............  {self.torrent.mytorr.location}')
                console.log(f'[TORRENT NAME]................  {self.torrent.mytorr.name}.torrent')
                return True
        console.log(f"Non ho trovato nessun torrents in list corrispondente al tuo {self.torrent.mytorr.name}")
        return False
