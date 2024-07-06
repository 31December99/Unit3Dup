# -*- coding: utf-8 -*-
import json
import os
import time
import sys
import typing
import torf
import requests
import logging
from decouple import Config, RepositoryEnv
from qbittorrent import Client
from tqdm import tqdm
from unit3dup.contents import Cli

logging.basicConfig(level=logging.INFO)

config_load = Config(RepositoryEnv('service.env'))
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

    def __init__(self, contents: Cli, meta: str, tracker_announce_list: list):

        self.qb = None
        self.file_name = contents.file_name
        self.torrent_path = contents.folder
        self.content_type = contents.category
        self.metainfo = json.loads(meta)
        self.__torrent_name = self.torrent_path if not self.content_type else os.path.join(self.torrent_path,
                                                                                           self.file_name)
        self.mytorr = torf.Torrent(path=self.__torrent_name)
        self.mytorr.announce_list = tracker_announce_list
        self.mytorr.comment = "ciao"
        self.mytorr.name = contents.file_name
        self.mytorr.created_by = "Unit3d-Up"
        self.mytorr.private = True
        self.mytorr.segments = 16 * 1024 * 1024  # 16MB

        print(f"[ HASHING ] {self.file_name}")
        with HashProgressBar() as progress:
            self.mytorr.generate(threads=0, callback=progress.callback, interval=0)
        print("\n")

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
            logging.info("Non è stato possibile collegarsi a qbittorent. Verifica WEBUI")
            logging.info(f"{e}")
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
                logging.info(f'[TORRENT INFOHASH]............  {infohash}')
                logging.info(f'[TORRENT LOCATION]............  {self.mytorr.location}')
                logging.info(f'[TORRENT NAME]................  {self.torrent_name}.torrent')
                return True
        logging.info(f"Non ho trovato nessun torrents in list corrispondente al tuo {self.mytorr.name}")
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
