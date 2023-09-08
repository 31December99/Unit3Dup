#!/usr/bin/env python3.9
import argparse
import os.path
import requests
import pvtTracker
import myTMDB
import pvtVideo
import pvtTorrent
import utitlity
import Contents
from decouple import config

ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')

class ITtorrents:

    def __init__(self):

        if not ITT_PASS_KEY or not ITT_API_TOKEN:
            print("il file .env non è stato configurato o i nomi delle variabili sono errate.")
            return

        self.Itt = pvtTracker.ITT(base_url="https://itatorrents.xyz/", api_token=ITT_API_TOKEN,
                                  pass_key=ITT_PASS_KEY)
        self.category = None

        parser = argparse.ArgumentParser(description='Commands', add_help=False)
        parser.add_argument('-serie', '--serie', nargs=1, type=str, help='Serie')
        parser.add_argument('-movie', '--movie', nargs=1, type=str, help='Movie')
        args = parser.parse_args()
        if args.serie:
            self.content = Contents.Args(args.serie)
            self.metainfo = self.content.folder()
            self.Itt.data['name'] = utitlity.Manage_titles.clean(self.content.base_name)
            self.myguess = myTMDB.Myguessit(self.content.base_name)
            self.tmdb_series = myTMDB.TmdbSeries(self.myguess)
            self.video_tmdb_id = self.tmdb_series.cerca()
            self.category = 2

        if args.movie:
            self.content = Contents.Args(args.movie)
            self.metainfo = self.content.file()
            self.Itt.data['name'] = utitlity.Manage_titles.clean(self.content.tracker_file_name)
            self.myguess = myTMDB.Myguessit(self.content.file_name)
            self.tmdb_movie = myTMDB.TmdbMovie(self.myguess)
            self.video_tmdb_id = self.tmdb_movie.cerca()
            self.category = 1

        self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=self.metainfo)
        self.video = pvtVideo.Video(fileName=os.path.join(self.content.path, self.content.file_name))
        self.torrent = self.mytorrent.write
        self.standard = self.video.standard
        self.media_info = self.video.mediainfo
        self.descrizione = self.video.description
        self.freelech = self.video.freeLech

        self.Itt.data['free'] = self.freelech
        self.Itt.data['sd'] = self.standard
        self.Itt.data['mediainfo'] = self.media_info
        self.Itt.data['description'] = self.descrizione
        self.Itt.data['type_id'] = utitlity.Manage_titles.filterType(self.content.file_name)
        self.Itt.data['season_number'] = int(self.myguess.guessit_season)
        self.Itt.data['episode_number'] = int(self.myguess.guessit_season)
        self.Itt.data['tmdb'] = self.video_tmdb_id
        self.Itt.data['category_id'] = self.category

        if not self.video_tmdb_id:
            while True:
                utitlity.Console.print("Non è stato possibile identificare il TMDB ID. Inserisci un numero..", 2)
                self.video_id = input("> ")
                if not self.video_id.isdigit():
                    continue
                utitlity.Console.print(f"Hai digitato {self.video_id}", 2)
                user_answ = input("Sei sicuro ? (s/n)> ")
                if 's' == user_answ.lower():
                    break

        tracker_response = self.Itt.upload_t(data=self.Itt.data, file_name=os.path.join(self.content.path,
                                                                                        self.mytorrent.read()))

        upload_success = tracker_response['success']

        if upload_success:
            link_torrent_dal_tracker = tracker_response['data']
            messaggio_dal_tracker = tracker_response['message']
            pvtTracker.Utility.console(upload_success, 2)
            pvtTracker.Utility.console(link_torrent_dal_tracker, 2)
            pvtTracker.Utility.console(messaggio_dal_tracker, 2)

            download_torrent_dal_tracker = requests.get(link_torrent_dal_tracker)
            if download_torrent_dal_tracker.status_code == 200:
                self.mytorrent.qbit(download_torrent_dal_tracker)

        else:
            pvtTracker.Utility.console(f"Non è stato possibile fare l'upload => {tracker_response}", 1)


if os.name == 'nt':
    os.system('color')

ittorrents = ITtorrents()
