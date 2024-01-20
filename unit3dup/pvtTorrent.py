# -*- coding: utf-8 -*-
import json
import os
import time
import sys
import typing
import torf
import requests
import logging
from decouple import config
from qbittorrent import Client
from tqdm import tqdm
from unit3dup import Contents

logging.basicConfig(level=logging.INFO)


BASE_URL = config('BASE_URL')
PASS_KEY = config('PASS_KEY')
API_TOKEN = config('API_TOKEN')
QBIT_USER = config('QBIT_USER')
QBIT_PASS = config('QBIT_PASS')
QBIT_PORT = config('QBIT_PORT')
TORRENTS_FOLDER = config('TORRENTS_FOLDER')


class HashProgressBar(tqdm):
    def callback(self, mytorr, path, current_num_hashed, total_pieces):
        progress_percentage = (current_num_hashed / total_pieces) * 100
        self.total = 100
        self.update(int(progress_percentage) - self.n)


class Mytorrent:

    def __init__(self, contents: Contents, meta: str):

        self.qb = None
        self.file_name = contents.file_name
        self.path = contents.path
        self.content_type = contents.type
        self.base_name = contents.base_name
        self.metainfo = json.loads(meta)
        self.paths = self.path if self.content_type else os.path.join(self.path, self.file_name)
        self.mytorr = torf.Torrent(path=self.paths)
        self.mytorr.announce_list = [f"{BASE_URL}/announce/{PASS_KEY}/"]
        self.mytorr.comment = "ciao"
        self.mytorr.name = self.file_name if not self.base_name else self.base_name
        self.mytorr.created_by = "bUnit"
        self.mytorr.private = True
        self.mytorr.segments = 16 * 1024 * 1024  # 16MB
        print(f"[ HASHING ]")
        with HashProgressBar() as progress:
            self.mytorr.generate(threads=0, callback=progress.callback, interval=0)
        print("\n")

    @property
    def write(self):
        torrent_name = os.path.join(self.path, self.file_name) \
            if not self.base_name else os.path.join(self.path, self.base_name)
        try:
            self.mytorr.write(f"{torrent_name}.torrent")
        except torf.TorfError as e:
            print(e)
            sys.exit()
        return self.mytorr

    def read(self) -> str:
        torrent_name = os.path.join(self.path, self.file_name) \
            if not self.base_name else os.path.join(self.path, self.base_name)
        return str(torrent_name)

    def _download(self, link: requests) -> typing.IO:
        torrent_name = os.path.join(self.path, self.file_name) \
            if not self.base_name else os.path.join(self.path, self.base_name)
        with open(f'{torrent_name}.torrent', 'wb') as file:
            file.write(link.content)
        return open(f'{torrent_name}.torrent', 'rb')

    def qbit(self, link: requests) -> bool:
        torrent_file = self._download(link)
        try:
            self.qb = Client(f'http://127.0.0.1:{QBIT_PORT}/')
        except Exception as e:  # todo
            logging.info("Non è stato possibile collegarsi a qbittorent. Verifica WEBUI")
            logging.info(f"{e}")
            return False

        self.qb.login(username=QBIT_USER, password=QBIT_PASS)
        self.qb.download_from_file(torrent_file)
        time.sleep(3)
        # Ottieni la lista dei torrent
        torrents = self.qb.torrents()
        # Trova il torrent desiderato
        for torrent in torrents:
            if torrent['name'] == self.mytorr.name:
                infohash = torrent['hash']
                # Location del torrent
                self.qb.set_torrent_location(infohash, TORRENTS_FOLDER)
                self.qb.recheck(infohash_list=infohash)
                logging.info(f'[TORRENT INFOHASH]............  {infohash}')
                logging.info(f'[TORRENT LOCATION]............  {self.mytorr.location}')
                return True
        logging.info(f"Non ho trovato nessun torrents in list corripondente al tuo {self.mytorr.name}")
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
