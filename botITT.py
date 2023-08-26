#!/usr/bin/env python3.9

import sys
import time
import requests
from pymediainfo import MediaInfo
from qbittorrent import Client
import pvtTorrent
import pvtTracker
import myTMDB
from decouple import config


ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')
QBIT_USER = config('QBIT_USER')
QBIT_PASS = config('QBIT_PASS')

class ITtorrents:

    def __init__(self, file_name: str):
        if not ITT_PASS_KEY or not ITT_API_TOKEN or not QBIT_PASS or not QBIT_USER:
            print("il file .env non è stato configurato o i nomi delle variabili sono errate.")
            return

        self.file_name = file_name
        self.Itt = pvtTracker.ITT(base_url="https://itatorrents.xyz/", api_token=ITT_API_TOKEN,
                                  pass_key=ITT_PASS_KEY)

        self.media_info = MediaInfo.parse(self.file_name, output="STRING", full=False)
        self.myguess = myTMDB.Myguessit(self.file_name)
        mytorrent = pvtTorrent.Mytorrent(file_name=self.file_name)
        mytorrent.announce_list = f"https://itatorrents.xyz/announce/{ITT_PASS_KEY}/"
        mytorrent.comment = "ciao"
        mytorrent.name = self.file_name
        mytorrent.write(self.file_name)

        try:
            self.qb = Client('http://127.0.0.1:58672/')
        except Exception:
            pvtTracker.Utility.console(f"Non riesco a connettermi con Qbittorent.", 1)
            sys.exit()
        self.qb.login(username=QBIT_USER, password=QBIT_PASS)

        descrizione = f"[center]\n"
        sc = pvtTorrent.Screenshot(file_name=self.file_name)
        sc.samples_n = 6
        for f in sc.frames:
            img_host = pvtTorrent.ImgBB(f)
            descrizione += f"[url={img_host.upload['data']['display_url']}][img=350]{img_host.upload['data']['display_url']}[/img][/url]"
        descrizione += "\n[/center]"

        self.Itt.data['mediainfo'] = self.media_info
        self.Itt.data['description'] = descrizione

        if 'movie' in self.myguess.type:
            self.Itt.data['name'] = self.myguess.guessit_title
            self.tmdb_movie = myTMDB.TmdbMovie(self.myguess)
            self.video_id = self.tmdb_movie.cerca()
            self.Itt.data['category_id'] = 1
        else:
            self.tmdb_series = myTMDB.TmdbSeries(self.myguess)
            self.video_id = self.tmdb_series.cerca()
            self.Itt.data['category_id'] = 2
            self.Itt.data['name'] = self.myguess.guessit_title
            self.Itt.data['season_number'] = self.myguess.guessit_season
            self.Itt.data['episode_number'] = self.myguess.guessit_episode

        open_torrent = open(f'{self.file_name}.torrent', 'rb')
        files = {'torrent': open_torrent}
        tracker_response = self.Itt.upload_t(file=files, data=self.Itt.data, video_id=self.video_id)
        upload_success = tracker_response['success']

        if upload_success:
            link_torrent_dal_tracker = tracker_response['data']
            messaggio_dal_tracker = tracker_response['message']
            pvtTracker.Utility.console(upload_success, 2)
            pvtTracker.Utility.console(link_torrent_dal_tracker, 2)
            pvtTracker.Utility.console(messaggio_dal_tracker, 2)
            download_torrent_dal_tracker = requests.get(link_torrent_dal_tracker)

            if download_torrent_dal_tracker.status_code == 200:
                with open(f'{self.file_name}.torrent', 'wb') as file:
                    file.write(download_torrent_dal_tracker.content)
                torrent_file = open(f'{self.file_name}.torrent', 'rb')
                self.qb.download_from_file(torrent_file)
                print("Attendi..")
                time.sleep(5)
                # Ottieni la lista dei torrent
                torrents = self.qb.torrents()
                # Trova il torrent desiderato
                infohash = None
                for torrent in torrents:
                    if torrent['name'] == mytorrent.name:
                        infohash = torrent['hash']
                        break
                pvtTracker.Utility.console(f'HASH: {infohash}...Finito', 2)
                self.qb.recheck(infohash_list=infohash)
                self.qb.set_automatic_torrent_management(infohash_list=infohash, enable='True')

        else:
            pvtTracker.Utility.console(f"Non è stato possibile fare l'upload => {tracker_response}", 1)