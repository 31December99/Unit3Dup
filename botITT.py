# -*- coding: utf-8 -*-
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
import logging
from typing import Type, Any
from search import SearchTvShow
from decouple import config
from database.trackers import ITT, SHAISL

logging.basicConfig(level=logging.INFO)

PASS_KEY = config('PASS_KEY')
API_TOKEN = config('API_TOKEN')
BASE_URL = config('BASE_URL')
TRACKER = config('TRACK_NAME')


class Bot:

    def __init__(self, data: Type[Any]):

        if not PASS_KEY or not API_TOKEN:
            print("il file .env non è stato configurato oppure i nomi delle variabili sono errate.")
            return

        print(f"\n[TRACKER]..............  {BASE_URL}")
        self.Itt = pvtTracker.ITT(base_url=BASE_URL, api_token=API_TOKEN,
                                  pass_key=PASS_KEY)
        self.category = None
        self.tracker_data = data()

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
            self.category = self.tracker_data.category['serie_tv']

        if args.movie:
            self.mytmdb = SearchTvShow('Movie')
            self.content = Contents.Args(args.movie)
            self.metainfo = self.content.file()
            self.Itt.data['name'] = utitlity.Manage_titles.clean(self.content.tracker_file_name)
            self.myguess = myTMDB.Myguessit(self.content.file_name)
            self.result = self.mytmdb.start(str(self.myguess.guessit_title))
            self.category = self.tracker_data.category['movie']

        self.Itt.data['tmdb'] = self.result.video_id
        self.Itt.data['keywords'] = self.result.keywords

        self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=self.metainfo)
        self.video = pvtVideo.Video(fileName=str(os.path.join(self.content.path, self.content.file_name)))
        self.torrent = self.mytorrent.write
        self.standard = self.video.standard
        self.media_info = self.video.mediainfo
        self.descrizione = self.video.description
        self.freelech = self.tracker_data.get_freelech(self.video.size)

        self.Itt.data['category_id'] = self.category
        self.Itt.data['resolution_id'] = self.tracker_data.filterResolution(self.content.file_name)
        self.Itt.data['free'] = self.freelech
        self.Itt.data['sd'] = self.standard
        self.Itt.data['mediainfo'] = self.media_info
        self.Itt.data['description'] = self.descrizione
        self.Itt.data['type_id'] = self.tracker_data.filterType(self.content.file_name)
        self.Itt.data['season_number'] = int(self.myguess.guessit_season)
        self.Itt.data['episode_number'] = int(self.myguess.guessit_season)

        tracker_response = self.Itt.upload_t(data=self.Itt.data, file_name=os.path.join(self.content.path,
                                                                                        self.mytorrent.read()))
        if tracker_response.status_code == 200:
            tracker_response_body = json.loads(tracker_response.text)
            logging.info(tracker_response_body['message'])
            download_torrent_dal_tracker = requests.get(tracker_response_body['data'])
            if download_torrent_dal_tracker.status_code == 200:
                self.mytorrent.qbit(download_torrent_dal_tracker)
        else:
            logging.info(f"Non è stato possibile fare l'upload => {tracker_response} {tracker_response.text}")


if __name__ == "__main__":
    trackers = {
        "itt": ITT,
        "shisl": SHAISL,
    }
    bot = Bot(trackers.get(TRACKER.lower()))
