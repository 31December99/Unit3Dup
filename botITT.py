#!/usr/bin/env python3.9
import argparse
import os.path
import sys
import time
import requests
from qbittorrent import Client
import pvtTracker
import myTMDB
import pvtVideo
from decouple import config

ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')
QBIT_USER = config('QBIT_USER')
QBIT_PASS = config('QBIT_PASS')
QBIT_PORT = config('QBIT_PORT')


class ITtorrents:

    def __init__(self, contents: str):

        if not ITT_PASS_KEY or not ITT_API_TOKEN or not QBIT_PASS or not QBIT_USER:
            print("il file .env non è stato configurato o i nomi delle variabili sono errate.")
            return

        self.Itt = pvtTracker.ITT(base_url="https://itatorrents.xyz/", api_token=ITT_API_TOKEN,
                                  pass_key=ITT_PASS_KEY)

        self.video = pvtVideo.Video(contents=contents)
        self.file_name = self.video.file_name
        self.standard = self.video.standard
        self.freelech = self.video.freeLech
        self.media_info = self.video.mediainfo
        self.descrizione = self.video.description
        self.torrent = self.video.torrent
        self.myguess = myTMDB.Myguessit(self.file_name)
        self.Itt.data['free'] = self.freelech
        self.Itt.data['sd'] = self.standard
        self.Itt.data['mediainfo'] = self.media_info
        self.Itt.data['description'] = self.descrizione

        if 'movie' in self.myguess.type:
            self.Itt.data['name'] = self.file_name.replace('.', ' ')
            self.tmdb_movie = myTMDB.TmdbMovie(self.myguess)
            self.video_id = self.tmdb_movie.cerca()
            self.Itt.data['category_id'] = 1
        else:
            self.tmdb_series = myTMDB.TmdbSeries(self.myguess)
            self.video_id = self.tmdb_series.cerca()
            self.Itt.data['category_id'] = 2
            self.Itt.data['name'] = self.file_name.replace('.', ' ')
            self.Itt.data['season_number'] = self.myguess.guessit_season
            self.Itt.data['episode_number'] = self.myguess.guessit_episode

        tracker_response = self.Itt.upload_t(data=self.Itt.data, video_id=self.video_id, file_name=self.file_name)
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

                try:
                    self.qb = Client(f'http://127.0.0.1:{QBIT_PORT}/')
                except Exception: # todo
                    pvtTracker.Utility.console(f"Non riesco a connettermi con Qbittorent.", 1)
                    sys.exit()
                self.qb.login(username=QBIT_USER, password=QBIT_PASS)

                self.qb.download_from_file(torrent_file)
                print("Attendi..")
                time.sleep(2)
                # Ottieni la lista dei torrent
                torrents = self.qb.torrents()
                # Trova il torrent desiderato
                infohash = None
                for torrent in torrents:
                    if torrent['name'] == self.torrent.name:
                        infohash = torrent['hash']
                        break
                pvtTracker.Utility.console(f'HASH: {infohash}...Finito', 2)
                self.qb.recheck(infohash_list=infohash)
                self.qb.set_automatic_torrent_management(infohash_list=infohash, enable='True')

        else:
            pvtTracker.Utility.console(f"Non è stato possibile fare l'upload => {tracker_response}", 1)


if os.name == 'nt':
    os.system('color')
parser = argparse.ArgumentParser(description='Commands', add_help=False)
parser.add_argument('-dw', '--dw', nargs=1, type=str, help='FileName')
args = parser.parse_args()
if args.dw:
    ittorrents = ITtorrents(args.dw[0])
