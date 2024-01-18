#!/usr/bin/env python3.9
import argparse
import json
import os.path
import requests
import pvtTracker
import myTMDB
import pvtVideo
import pvtTorrent
import utitlity
import Contents
from search import SearchTvShow
from decouple import config

ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')
ITT_BASE_URL = config('ITT_BASE_URL')


class ITtorrents:

    def __init__(self):

        if not ITT_PASS_KEY or not ITT_API_TOKEN:
            print("il file .env non è stato configurato o i nomi delle variabili sono errate.")
            return

        self.Itt = pvtTracker.ITT(base_url=ITT_BASE_URL, api_token=ITT_API_TOKEN,
                                  pass_key=ITT_PASS_KEY)
        self.category = None

        parser = argparse.ArgumentParser(description='Commands', add_help=False)
        parser.add_argument('-serie', '--serie', nargs=1, type=str, help='Serie')
        parser.add_argument('-movie', '--movie', nargs=1, type=str, help='Movie')
        args = parser.parse_args()
        if args.serie:
            self.mytmdb = SearchTvShow('Serie')
            self.content = Contents.Args(args.serie)
            self.metainfo = self.content.folder()
            self.Itt.data['name'] = utitlity.Manage_titles.clean(self.content.base_name)
            self.myguess = myTMDB.Myguessit(self.content.file_name)
            self.result = self.mytmdb.start(str(self.myguess.guessit_title))
            self.category = 2

        if args.movie:
            self.mytmdb = SearchTvShow('Movie')
            self.content = Contents.Args(args.movie)
            self.metainfo = self.content.file()
            self.Itt.data['name'] = utitlity.Manage_titles.clean(self.content.tracker_file_name)
            self.myguess = myTMDB.Myguessit(self.content.file_name)
            self.result = self.mytmdb.start(str(self.myguess.guessit_title))
            self.category = 1

        self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=self.metainfo)
        self.video = pvtVideo.Video(fileName=str(os.path.join(self.content.path, self.content.file_name)))
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
        if self.result:
            self.Itt.data['tmdb'] = self.result.video_id
        self.Itt.data['category_id'] = self.category
        self.Itt.data['resolution_id'] = utitlity.Manage_titles.filterResolution(self.content.file_name)

        if not self.result:
            while True:
                utitlity.Console.print("Non è stato possibile identificare il TMDB ID. Inserisci un numero..", 2)
                self.video_tmdb_id = input(f"> ")
                if not self.video_tmdb_id.isdigit():
                    continue
                utitlity.Console.print(f"Hai digitato {self.video_tmdb_id}", 2)
                user_answ = input("Sei sicuro ? (s/n)> ")
                if 's' == user_answ.lower():
                    self.Itt.data['tmdb'] = self.video_tmdb_id
                    keywords = self.mytmdb.get_keywords(int(self.video_tmdb_id))
                    if 'The resource you requested could not be found.' not in keywords:
                        self.Itt.data['keywords'] = keywords
                        break
                    print("Riprova... ")
        else:
            self.Itt.data['keywords'] = self.result.keywords

        tracker_response = self.Itt.upload_t(data=self.Itt.data, file_name=os.path.join(self.content.path,
                                                                                        self.mytorrent.read()))
        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            pvtTracker.Utility.console(tracker_response_body['message'], 2)
            download_torrent_dal_tracker = requests.get(tracker_response_body['data'])
            if download_torrent_dal_tracker.status_code == 200:
                self.mytorrent.qbit(download_torrent_dal_tracker)
        else:
            pvtTracker.Utility.console(f"Non è stato possibile fare l'upload => {tracker_response}", 1)


if os.name == 'nt':
    os.system('color')

ittorrents = ITtorrents()
