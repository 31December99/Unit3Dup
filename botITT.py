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
from search import SearchTvShow
from decouple import config

logging.basicConfig(level=logging.INFO)

ITT_PASS_KEY = config('ITT_PASS_KEY')
ITT_API_TOKEN = config('ITT_API_TOKEN')
ITT_BASE_URL = config('ITT_BASE_URL')


class ITtorrents:

    def __init__(self):

        if not ITT_PASS_KEY or not ITT_API_TOKEN:
            print("il file .env non è stato configurato o i nomi delle variabili sono errate.")
            return

        print(f"\n[TRACKER]..............  {ITT_BASE_URL}")
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

            self.Itt.data['tmdb'] = self.result.video_id
            self.Itt.data['keywords'] = self.result.keywords

        self.mytorrent = pvtTorrent.Mytorrent(contents=self.content, meta=self.metainfo)
        self.video = pvtVideo.Video(fileName=str(os.path.join(self.content.path, self.content.file_name)))
        self.torrent = self.mytorrent.write
        self.standard = self.video.standard
        self.media_info = self.video.mediainfo
        self.descrizione = self.video.description
        self.freelech = self.video.freeLech

        self.Itt.data['category_id'] = self.category
        self.Itt.data['resolution_id'] = utitlity.Manage_titles.filterResolution(self.content.file_name)
        self.Itt.data['free'] = self.freelech
        self.Itt.data['sd'] = self.standard
        self.Itt.data['mediainfo'] = self.media_info
        self.Itt.data['description'] = self.descrizione
        self.Itt.data['type_id'] = utitlity.Manage_titles.filterType(self.content.file_name)
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


if os.name == 'nt':
    os.system('color')

if __name__ == "__main__":
    ittorrents = ITtorrents()
