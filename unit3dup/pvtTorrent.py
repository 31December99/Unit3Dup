# -*- coding: utf-8 -*-
import json
import os
import time
import sys
import typing
import torf
import requests
from decouple import Config, RepositoryEnv
from qbittorrent import Client
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
    """
    Crea un torrent per serie o movie

    movie: occorre fornire il percorso completo fino al file con estensione
    serie: ogni episodio anche singolo deve essere contenuto in una cartella che ha come nome il titolo della serie o
            di un episodio della serie
    """

    def __init__(self, contents: Contents, meta: str):

        self.qb = None
        self.file_name = contents.file_name
        self.torrent_path = contents.folder
        self.basename = os.path.basename(self.torrent_path)
        self.content_type = contents.category
        self.metainfo = json.loads(meta)
        self.__torrent_name = self.torrent_path if self.content_type == 2 else os.path.join(self.torrent_path,
                                                                                            self.file_name)
        self.mytorr = torf.Torrent(path=self.__torrent_name)
        self.mytorr.comment = "ciao"
        self.mytorr.name = self.basename if self.content_type == 2 else contents.file_name
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
            self.mytorr.write(f"{self.torrent_name}.torrent")
        except torf.TorfError as e:
            print(e)
            sys.exit()
        return self.mytorr

    def _download(self, link: requests) -> typing.IO:
        with open(f'{self.torrent_name}.torrent', 'wb') as file:
            file.write(link.content)
        return open(f'{self.torrent_name}.torrent', 'rb')

    def qbit(self, link: requests) -> bool:
        torrent_file = self._download(link)
        try:
            self.qb = Client(f'{QBIT_URL}:{QBIT_PORT}/')
        except Exception as e:  # todo
            console.log("Non è stato possibile collegarsi a qbittorent. Verifica WEBUI")
            console.log(f"{e}")
            return False

        self.qb.login(username=QBIT_USER, password=QBIT_PASS)
        self.qb.download_from_file(file_buffer=torrent_file, savepath=self.mytorr.location)
        time.sleep(3)
        # Ottieni la lista dei torrent
        torrents = self.qb.torrents()
        # Trova il torrent desiderato
        for torrent in torrents:
            if torrent['name'] == self.mytorr.name:
                infohash = torrent['hash']
                # Location del torrent
                self.qb.recheck(infohash_list=infohash)
                console.log(f'\n[TORRENT INFOHASH]............  {infohash}')
                console.log(f'[TORRENT LOCATION]............  {self.mytorr.location}')
                console.log(f'[TORRENT NAME]................  {self.mytorr.name}.torrent')
                return True
        console.log(f"Non ho trovato nessun torrents in list corrispondente al tuo {self.mytorr.name}")
        return False

    @property
    def torrent_name(self) -> str:
        return self.__torrent_name

    @property
    def comment(self):
        return self.mytorr.comment

    @comment.setter
    def comment(self, value):
        self.mytorr.comment = value

    @property
    def info_hash(self):
        return self.mytorr.infohash
