# -*- coding: utf-8 -*-
import argparse
import json
import os.path
import requests
import logging
from typing import Type, Any
from decouple import config
from database.trackers import ITT, SHAISL
from unit3dup import pvtTracker, myTMDB, pvtVideo, pvtTorrent, utitlity, Contents, search

logging.basicConfig(level=logging.INFO)

PASS_KEY = config('PASS_KEY')
API_TOKEN = config('API_TOKEN')
BASE_URL = config('BASE_URL')
TRACKER_NAME = config('TRACK_NAME')

trackers = {
    "itt": ITT,
    "shaisl": SHAISL,
}


class Bot:
    def __init__(self, data: Type[Any], args: argparse):

        if not PASS_KEY or not API_TOKEN:
            logging.info("il file .env non è stato configurato oppure i nomi delle variabili sono errate.")
            return
        if not data:
            print("[BOT] Non riconosco il nome del tracker che hai impostato nel file .env di configurazione\n"
                  "[BOT] Di seguito i nomi disponibili per il tuo tracker:")
            for tracker in trackers:
                print(f"[BOT] <{tracker}>")
            print("[BOT] Verifica ora il tuo file .env")
            return

        if not args.serie and not args.movie:
            print("Devi scegliere tra --movie e --serie. Esempio 'start.py -serie' seguito dal percorso completo")
            return

        print(f"\n[TRACKER]..............  {BASE_URL}")
        self.tracker_values = data()

        # // Options
        if args.serie:
            self.mytmdb = search.TvShow('Serie')
            self.content = Contents.Args(args.serie)
            self.metainfo = self.content.folder()
            self.name = utitlity.Manage_titles.clean(self.content.base_name)
            self.myguess = myTMDB.Myguessit(self.content.file_name)
            self.result = self.mytmdb.start(str(self.myguess.guessit_title))
            self.category = self.tracker_values.category['serie_tv']

        if args.movie:
            self.mytmdb = search.TvShow('Movie')
            self.content = Contents.Args(args.movie)
            self.metainfo = self.content.file()
            self.name = utitlity.Manage_titles.clean(self.content.tracker_file_name)
            self.myguess = myTMDB.Myguessit(self.content.file_name)
            self.result = self.mytmdb.start(str(self.myguess.guessit_title))
            self.category = self.tracker_values.category['movie']

        # // Video data
        self.video = pvtVideo.Video(fileName=str(os.path.join(self.content.path, self.content.file_name)))
        self.standard = self.video.standard
        self.media_info = self.video.mediainfo
        self.descrizione = self.video.description
        self.freelech = self.tracker_values.get_freelech(self.video.size)

        # // Tracker data
        self.tracker = pvtTracker.ITT(base_url=BASE_URL, api_token=API_TOKEN, pass_key=PASS_KEY)
        self.tracker.data['name'] = self.name
        self.tracker.data['tmdb'] = self.result.video_id
        self.tracker.data['keywords'] = self.result.keywords
        self.tracker.data['category_id'] = self.category
        self.tracker.data['resolution_id'] = self.tracker_values.filterResolution(self.content.file_name)
        self.tracker.data['free'] = self.freelech
        self.tracker.data['sd'] = self.standard
        self.tracker.data['mediainfo'] = self.media_info
        self.tracker.data['description'] = self.descrizione
        self.tracker.data['type_id'] = self.tracker_values.filterType(self.content.file_name)
        self.tracker.data['season_number'] = int(self.myguess.guessit_season)
        self.tracker.data['episode_number'] = int(self.myguess.guessit_season)

        # // Torrent
        self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=self.metainfo)
        self.torrent = self.mytorrent.write

        # // Send data
        tracker_response = self.tracker.upload_t(data=self.tracker.data, file_name=os.path.join(self.content.path,
                                                                                                self.mytorrent.read()))
        # // Seeding
        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            logging.info(tracker_response_body['message'])
            download_torrent_dal_tracker = requests.get(tracker_response_body['data'])
            if download_torrent_dal_tracker.status_code == 200:
                self.mytorrent.qbit(download_torrent_dal_tracker)
        else:
            logging.info(f"Non è stato possibile fare l'upload => {tracker_response} {tracker_response.text}")
