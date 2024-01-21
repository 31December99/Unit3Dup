# -*- coding: utf-8 -*-
import argparse
import json
import os.path
import requests
import logging
from decouple import Config, RepositoryEnv
from database.trackers import TrackerConfig
from unit3dup import pvtTracker, pvtVideo, pvtTorrent, utitlity, Contents, search, title

logging.basicConfig(level=logging.INFO)


class UploadBot:
    def __init__(self, args: argparse):

        # // check command line
        if not args.serie and not args.movie or not args.tracker:
            print("Esempio 'serie' 'start.py -s' <percorso completo cartella>\n"
                  "Esempio 'movie' 'start.py -m' <percorso completo file>\n"
                  "Esempio 'start.py -t hello -s [...] dove '-t' rappresenta il nome del tracker e non l'indirizzo "
                  "http.")
            return

        # // check tracker file configuration .env e .json

        self.tracker_env = f"{args.tracker[0]}.env"
        if not os.path.exists(self.tracker_env):
            print(f"\n[.ENV] Non trovo il file '{self.tracker_env}' per caricare api_key e token")
            return

        config_load = Config(RepositoryEnv(self.tracker_env))
        PASS_KEY = config_load('PASS_KEY')
        API_TOKEN = config_load('API_TOKEN')
        BASE_URL = config_load('BASE_URL')

        print(PASS_KEY, API_TOKEN, BASE_URL)

        if not PASS_KEY or not API_TOKEN:
            logging.info("il file .env non è stato configurato oppure i nomi delle variabili sono errate.")
            return

        self.tracker_json = f"{args.tracker[0]}.json"
        if not os.path.exists(self.tracker_json):
            print(f"\n[TRACKER] Non trovo il tracker '{self.tracker_json}'")
            return

        self.tracker_values = TrackerConfig(self.tracker_json)
        print(f"\n[TRACKER {args.tracker[0]}]..............  {BASE_URL}")

        # // Options
        if args.serie:
            self.mytmdb = search.TvShow('Serie')
            self.content = Contents.Args(args.serie)
            self.metainfo = self.content.folder()
            self.name = utitlity.Manage_titles.clean(self.content.base_name)
            self.myguess = title.Guessit(self.content.file_name)
            self.result = self.mytmdb.start(str(self.myguess.guessit_title))
            self.category = self.tracker_values.category('tvshow')

        if args.movie:
            self.mytmdb = search.TvShow('Movie')
            self.content = Contents.Args(args.movie)
            self.metainfo = self.content.file()
            self.name = utitlity.Manage_titles.clean(self.content.tracker_file_name)
            self.myguess = title.Guessit(self.content.file_name)
            self.result = self.mytmdb.start(str(self.myguess.guessit_title))
            self.category = self.tracker_values.category('movie')

        # // Video data
        self.video = pvtVideo.Video(fileName=str(os.path.join(self.content.path, self.content.file_name)))
        self.standard = self.video.standard
        self.media_info = self.video.mediainfo
        self.descrizione = self.video.description
        self.freelech = self.tracker_values.get_freelech(self.video.size)

        # // Tracker data
        self.tracker = pvtTracker.Unit3d(base_url=BASE_URL, api_token=API_TOKEN, pass_key=PASS_KEY)
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
        self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=self.metainfo,
                                              tracker_announce_list=[f"{BASE_URL}/announce/{PASS_KEY}/"])
        self.mytorrent.write()

        # // Send data
        tracker_response = self.tracker.upload_t(data=self.tracker.data, file_name=os.path.join(self.content.path,
                                                                                                self.mytorrent.read()))
        # // Seeding
        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            logging.info(f"[TRACKER RESPONSE].............. {tracker_response_body['message'].upper()}")
            download_torrent_dal_tracker = requests.get(tracker_response_body['data'])
            if download_torrent_dal_tracker.status_code == 200:
                self.mytorrent.qbit(download_torrent_dal_tracker)
        else:
            logging.info(f"Non è stato possibile fare l'upload => {tracker_response} {tracker_response.text}")
